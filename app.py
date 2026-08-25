import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
from supabase import create_client, Client
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# SUPABASE SETUP
# ============================================================================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Missing Supabase credentials. Set SUPABASE_URL and SUPABASE_KEY in .env")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Mileage Tracker",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS STYLING
# ============================================================================
st.markdown("""
<style>
    [data-testid="stMetricDelta"] {
        font-size: 18px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 5px;
        color: #155724;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 5px;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def hash_password(password):
    """Hash password for storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_authentication():
    """Check if user is logged in"""
    return "user_id" in st.session_state and st.session_state.user_id is not None

def get_user_vehicles():
    """Get all vehicles for current user"""
    try:
        response = supabase.table("vehicles").select("*").eq("user_id", st.session_state.user_id).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error fetching vehicles: {e}")
        return []

def get_vehicle_records(vehicle_id):
    """Get all fuel records for a vehicle"""
    try:
        response = supabase.table("fuel_records").select("*").eq("vehicle_id", vehicle_id).order("date", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error fetching records: {e}")
        return []

def calculate_mileage(distance_km, fuel_liters):
    """Calculate mileage"""
    if fuel_liters > 0:
        return round(distance_km / fuel_liters, 2)
    return 0

def calculate_cost_per_km(cost, distance_km):
    """Calculate cost per kilometer"""
    if distance_km > 0:
        return round(cost / distance_km, 2)
    return 0

def signup_user(email, password):
    """Register new user"""
    try:
        # Check if user exists
        response = supabase.table("users").select("id").eq("email", email).execute()
        if response.data:
            return False, "Email already registered"
        
        # Create user
        response = supabase.table("users").insert({
            "email": email,
            "password_hash": hash_password(password),
            "created_at": datetime.now().isoformat()
        }).execute()
        
        if response.data:
            return True, "Signup successful"
        return False, "Signup failed"
    except Exception as e:
        return False, f"Error: {e}"

def login_user(email, password):
    """Authenticate user"""
    try:
        response = supabase.table("users").select("id, password_hash").eq("email", email).execute()
        
        if not response.data:
            return False, None, "Email not found"
        
        user = response.data[0]
        if user["password_hash"] == hash_password(password):
            return True, user["id"], "Login successful"
        return False, None, "Invalid password"
    except Exception as e:
        return False, None, f"Error: {e}"

def add_fuel_record(vehicle_id, date, fuel_liters, current_km, last_refuel_km, cost):
    """Add new fuel record"""
    try:
        distance_km = current_km - last_refuel_km
        mileage = calculate_mileage(distance_km, fuel_liters)
        cost_per_km = calculate_cost_per_km(cost, distance_km)
        
        response = supabase.table("fuel_records").insert({
            "vehicle_id": vehicle_id,
            "date": date.isoformat(),
            "fuel_filled_litres": fuel_liters,
            "current_odometer_km": current_km,
            "last_refuel_km": last_refuel_km,
            "cost_rupees": cost,
            "distance_km": distance_km,
            "mileage_km_per_litre": mileage,
            "cost_per_km": cost_per_km,
            "created_at": datetime.now().isoformat()
        }).execute()
        
        return True, "Record added successfully"
    except Exception as e:
        return False, f"Error: {e}"

def delete_record(record_id):
    """Delete a fuel record"""
    try:
        supabase.table("fuel_records").delete().eq("id", record_id).execute()
        return True, "Record deleted"
    except Exception as e:
        return False, f"Error: {e}"

def add_vehicle(car_model, registration):
    """Add new vehicle"""
    try:
        response = supabase.table("vehicles").insert({
            "user_id": st.session_state.user_id,
            "vehicle_name": car_model,
            "model": car_model,
            "registration": registration,
            "created_at": datetime.now().isoformat()
        }).execute()
        
        if response.data:
            return True, "Vehicle added"
        return False, "Failed to add vehicle"
    except Exception as e:
        return False, f"Error: {e}"

def import_excel_data(vehicle_id, file):
    """Import fuel records from Excel"""
    try:
        df = pd.read_excel(file)
        
        # Expected columns
        required_cols = ['Date', 'Mieleage KM', 'Qty (Ltr)', 'Rate', 'Total Cost']
        
        # Skip first few rows if needed
        df = df.iloc[3:].reset_index(drop=True)
        
        records_added = 0
        errors = []
        
        for idx, row in df.iterrows():
            try:
                if pd.isna(row.iloc[0]):
                    continue
                
                date = pd.to_datetime(row.iloc[0])
                current_km = float(row.iloc[1])
                fuel_liters = float(row.iloc[2])
                cost = float(row.iloc[4])
                
                # Calculate last_refuel_km (assume previous row's current_km)
                if idx > 0:
                    last_refuel_km = float(df.iloc[idx-1, 1])
                else:
                    last_refuel_km = current_km - (fuel_liters * 12)  # Estimate
                
                success, msg = add_fuel_record(vehicle_id, date, fuel_liters, current_km, last_refuel_km, cost)
                if success:
                    records_added += 1
                else:
                    errors.append(f"Row {idx}: {msg}")
            except Exception as e:
                errors.append(f"Row {idx}: {str(e)}")
        
        return records_added, errors
    except Exception as e:
        return 0, [str(e)]

# ============================================================================
# AUTHENTICATION PAGES
# ============================================================================

def show_auth_page():
    """Show login/signup page"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Login")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login", key="login_btn"):
            success, user_id, msg = login_user(login_email, login_password)
            if success:
                st.session_state.user_id = user_id
                st.session_state.user_email = login_email
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
    
    with col2:
        st.subheader("Sign Up")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_pass")
        signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")
        
        if st.button("Sign Up", key="signup_btn"):
            if signup_password != signup_confirm:
                st.error("Passwords don't match")
            elif len(signup_password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                success, msg = signup_user(signup_email, signup_password)
                if success:
                    st.success(msg)
                    st.info("Now log in with your credentials")
                else:
                    st.error(msg)

# ============================================================================
# MAIN APP PAGES
# ============================================================================

def show_dashboard():
    """Main dashboard"""
    vehicles = get_user_vehicles()
    
    if not vehicles:
        st.warning("No vehicles added yet. Add a vehicle to get started.")
        return
    
    # Vehicle selector
    vehicle_options = {v["id"]: v["model"] for v in vehicles}
    if "selected_vehicle" not in st.session_state:
        st.session_state.selected_vehicle = vehicles[0]["id"]
    
    selected_vehicle_id = st.selectbox(
        "Select Vehicle",
        options=list(vehicle_options.keys()),
        format_func=lambda x: vehicle_options[x],
        key="vehicle_selector"
    )
    st.session_state.selected_vehicle = selected_vehicle_id
    
    # Get records for selected vehicle
    records = get_vehicle_records(selected_vehicle_id)
    
    if not records:
        st.info("No fuel records yet. Add your first entry.")
        return
    
    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date', ascending=False)
    
    # Quick Stats
    st.subheader("📊 Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    latest = df.iloc[0]
    
    with col1:
        st.metric("Last Mileage", f"{latest['mileage_km_per_litre']} KM/L")
    
    with col2:
        st.metric("Cost per KM", f"₹{latest['cost_per_km']}")
    
    with col3:
        month_avg = df[df['date'] >= datetime.now() - timedelta(days=30)]['mileage_km_per_litre'].mean()
        st.metric("This Month Avg", f"{month_avg:.2f} KM/L")
    
    with col4:
        month_cost = df[df['date'] >= datetime.now() - timedelta(days=30)]['cost_rupees'].sum()
        st.metric("This Month Cost", f"₹{month_cost:.0f}")
    
    # Trend Chart
    st.subheader("📈 Mileage Trend (Last 30 Days)")
    recent_df = df[df['date'] >= datetime.now() - timedelta(days=30)].sort_values('date')
    
    if len(recent_df) > 0:
        fig = px.line(recent_df, x='date', y='mileage_km_per_litre', 
                     markers=True, title="Mileage Over Time",
                     labels={'mileage_km_per_litre': 'Mileage (KM/L)', 'date': 'Date'})
        fig.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent Entries
    st.subheader("📋 Recent Entries")
    display_df = df[['date', 'fuel_filled_litres', 'distance_km', 'mileage_km_per_litre', 'cost_rupees', 'cost_per_km']].copy()
    display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
    display_df.columns = ['Date', 'Fuel (L)', 'Distance (KM)', 'Mileage', 'Cost (₹)', 'Cost/KM']
    
    st.dataframe(display_df.head(10), use_container_width=True)
    
    # Delete option
    if st.checkbox("Show delete options"):
        delete_idx = st.selectbox("Select record to delete", range(len(df)))
        if st.button("Delete Selected Record"):
            success, msg = delete_record(df.iloc[delete_idx]['id'])
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

def show_add_entry():
    """Add new fuel entry"""
    vehicles = get_user_vehicles()
    
    if not vehicles:
        st.warning("Add a vehicle first")
        return
    
    vehicle_options = {v["id"]: v["model"] for v in vehicles}
    selected_vehicle = st.selectbox("Select Vehicle", options=list(vehicle_options.keys()),
                                   format_func=lambda x: vehicle_options[x])
    
    st.subheader("➕ Add Fuel Entry")
    
    col1, col2 = st.columns(2)
    
    with col1:
        entry_date = st.date_input("Date", value=datetime.now())
        fuel_liters = st.number_input("Fuel Filled (Liters)", min_value=0.1, step=0.1)
    
    with col2:
        current_km = st.number_input("Current Odometer (KM)", min_value=0.0, step=1.0)
        last_refuel_km = st.number_input("Last Refuel KM", min_value=0.0, step=1.0)
    
    cost = st.number_input("Cost Paid (₹)", min_value=0.0, step=10.0)
    
    if st.button("✓ Save Entry"):
        distance = current_km - last_refuel_km
        if distance <= 0:
            st.error("Current KM must be greater than Last Refuel KM")
        else:
            success, msg = add_fuel_record(selected_vehicle, entry_date, fuel_liters, current_km, last_refuel_km, cost)
            if success:
                mileage = calculate_mileage(distance, fuel_liters)
                st.success(msg)
                st.metric("Calculated Mileage", f"{mileage} KM/L")
                st.rerun()
            else:
                st.error(msg)

def show_analytics():
    """Analytics page"""
    vehicles = get_user_vehicles()
    
    if not vehicles:
        st.warning("No vehicles added yet")
        return
    
    vehicle_options = {v["id"]: v["model"] for v in vehicles}
    selected_vehicle = st.selectbox("Select Vehicle", options=list(vehicle_options.keys()),
                                   format_func=lambda x: vehicle_options[x])
    
    records = get_vehicle_records(selected_vehicle)
    
    if not records:
        st.info("No data yet")
        return
    
    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'])
    
    st.subheader("📊 Analytics")
    
    # Weekly Stats
    st.markdown("### Weekly Stats")
    col1, col2, col3 = st.columns(3)
    
    weekly_df = df[df['date'] >= datetime.now() - timedelta(days=7)]
    if len(weekly_df) > 0:
        with col1:
            st.metric("Average", f"{weekly_df['mileage_km_per_litre'].mean():.2f} KM/L")
        with col2:
            st.metric("Best", f"{weekly_df['mileage_km_per_litre'].max():.2f} KM/L")
        with col3:
            st.metric("Worst", f"{weekly_df['mileage_km_per_litre'].min():.2f} KM/L")
    
    # Monthly Stats
    st.markdown("### Monthly Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    monthly_df = df[df['date'] >= datetime.now() - timedelta(days=30)]
    if len(monthly_df) > 0:
        with col1:
            st.metric("Average", f"{monthly_df['mileage_km_per_litre'].mean():.2f} KM/L")
        with col2:
            st.metric("Total Cost", f"₹{monthly_df['cost_rupees'].sum():.0f}")
        with col3:
            st.metric("Total KM", f"{monthly_df['distance_km'].sum():.0f}")
        with col4:
            avg_cost_per_km = monthly_df['cost_per_km'].mean()
            st.metric("Avg Cost/KM", f"₹{avg_cost_per_km:.2f}")
    
    # Yearly Stats
    st.markdown("### Yearly Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    yearly_df = df[df['date'] >= datetime.now() - timedelta(days=365)]
    if len(yearly_df) > 0:
        with col1:
            st.metric("Average", f"{yearly_df['mileage_km_per_litre'].mean():.2f} KM/L")
        with col2:
            st.metric("Total Cost", f"₹{yearly_df['cost_rupees'].sum():.0f}")
        with col3:
            st.metric("Total KM", f"{yearly_df['distance_km'].sum():.0f}")
        with col4:
            # CO2 emissions (assuming 2.3 kg CO2 per liter of fuel)
            co2_emissions = yearly_df['fuel_filled_litres'].sum() * 2.3
            st.metric("CO2 Emissions", f"{co2_emissions:.1f} kg")
    
    # Full trend chart
    st.markdown("### 90-Day Trend")
    trend_df = df[df['date'] >= datetime.now() - timedelta(days=90)].sort_values('date')
    
    if len(trend_df) > 0:
        fig = px.line(trend_df, x='date', y='mileage_km_per_litre',
                     markers=True, title="Mileage Trend",
                     labels={'mileage_km_per_litre': 'Mileage (KM/L)', 'date': 'Date'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def show_import():
    """Import Excel data"""
    vehicles = get_user_vehicles()
    
    if not vehicles:
        st.warning("Add a vehicle first")
        return
    
    vehicle_options = {v["id"]: v["model"] for v in vehicles}
    selected_vehicle = st.selectbox("Select Vehicle", options=list(vehicle_options.keys()),
                                   format_func=lambda x: vehicle_options[x])
    
    st.subheader("📥 Import Excel Data")
    
    uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        # Preview
        df_preview = pd.read_excel(uploaded_file, sheet_name=0)
        st.write("Preview (first 10 rows):")
        st.dataframe(df_preview.head(10))
        
        if st.button("✓ Confirm Import"):
            with st.spinner("Importing..."):
                records_added, errors = import_excel_data(selected_vehicle, uploaded_file)
            
            st.success(f"✓ Imported {records_added} records")
            
            if errors:
                st.warning(f"⚠️ {len(errors)} errors:")
                for err in errors[:5]:  # Show first 5 errors
                    st.text(err)
            
            st.rerun()

def show_vehicles():
    """Manage vehicles"""
    st.subheader("🚗 My Vehicles")
    
    vehicles = get_user_vehicles()
    
    if vehicles:
        for vehicle in vehicles:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{vehicle['model']}** - {vehicle['registration']}")
            with col2:
                st.text(f"Added: {vehicle['created_at'][:10]}")
    
    st.divider()
    st.subheader("➕ Add New Vehicle")
    
    car_model = st.text_input("Car Model", placeholder="e.g., Maruti Swift")
    registration = st.text_input("Registration Number (Optional)", placeholder="e.g., MH01AB1234")
    
    if st.button("Add Vehicle"):
        if not car_model:
            st.error("Car model is required")
        else:
            success, msg = add_vehicle(car_model, registration)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

def show_export():
    """Export data"""
    vehicles = get_user_vehicles()
    
    if not vehicles:
        st.warning("No vehicles to export")
        return
    
    vehicle_options = {v["id"]: v["model"] for v in vehicles}
    selected_vehicle = st.selectbox("Select Vehicle", options=list(vehicle_options.keys()),
                                   format_func=lambda x: vehicle_options[x])
    
    records = get_vehicle_records(selected_vehicle)
    
    if records:
        df = pd.DataFrame(records)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"fuel_records_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No records to export")

def show_profile():
    """User profile"""
    st.subheader("👤 Profile")
    
    st.write(f"**Email:** {st.session_state.user_email}")
    st.write(f"**Member Since:** {datetime.now().strftime('%Y-%m-%d')}")
    
    vehicles = get_user_vehicles()
    st.write(f"**Total Vehicles:** {len(vehicles)}")
    
    st.divider()
    
    if st.button("🔓 Logout", key="logout_btn"):
        st.session_state.user_id = None
        st.session_state.user_email = None
        st.success("Logged out")
        st.rerun()

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.title("🚗 Mileage Tracker")
    
    # Initialize session state
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    
    # Check authentication
    if not check_authentication():
        show_auth_page()
    else:
        # Sidebar navigation
        st.sidebar.title("Navigation")
        
        page = st.sidebar.radio(
            "Select Page",
            ["Dashboard", "Add Entry", "Analytics", "My Vehicles", "Import Data", "Export", "Profile"],
            key="nav_radio"
        )
        
        if page == "Dashboard":
            show_dashboard()
        elif page == "Add Entry":
            show_add_entry()
        elif page == "Analytics":
            show_analytics()
        elif page == "My Vehicles":
            show_vehicles()
        elif page == "Import Data":
            show_import()
        elif page == "Export":
            show_export()
        elif page == "Profile":
            show_profile()

if __name__ == "__main__":
    main()
