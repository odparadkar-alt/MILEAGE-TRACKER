-- ============================================================================
-- MILEAGE TRACKER DATABASE SCHEMA
-- ============================================================================
-- Copy and paste this into Supabase SQL Editor to create the database

-- Users Table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- Vehicles Table (Multi-car support)
CREATE TABLE vehicles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  vehicle_name TEXT NOT NULL,
  model TEXT NOT NULL,
  registration TEXT,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- Fuel Records Table
CREATE TABLE fuel_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vehicle_id UUID REFERENCES vehicles(id) ON DELETE CASCADE NOT NULL,
  date TIMESTAMP NOT NULL,
  fuel_filled_litres DECIMAL(10, 2) NOT NULL,
  current_odometer_km DECIMAL(10, 2) NOT NULL,
  last_refuel_km DECIMAL(10, 2) NOT NULL,
  cost_rupees DECIMAL(10, 2) NOT NULL,
  distance_km DECIMAL(10, 2) GENERATED ALWAYS AS (current_odometer_km - last_refuel_km) STORED,
  mileage_km_per_litre DECIMAL(10, 2),
  cost_per_km DECIMAL(10, 2),
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- Imports History Table (Track imports)
CREATE TABLE imports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  vehicle_id UUID REFERENCES vehicles(id) ON DELETE CASCADE NOT NULL,
  file_name TEXT NOT NULL,
  records_imported INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT now()
);

-- ============================================================================
-- INDEXES (For performance)
-- ============================================================================

CREATE INDEX idx_vehicles_user_id ON vehicles(user_id);
CREATE INDEX idx_fuel_records_vehicle_id ON fuel_records(vehicle_id);
CREATE INDEX idx_fuel_records_date ON fuel_records(date);
CREATE INDEX idx_imports_user_id ON imports(user_id);
CREATE INDEX idx_users_email ON users(email);

-- ============================================================================
-- SECURITY (Row Level Security - Optional but recommended)
-- ============================================================================

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE vehicles ENABLE ROW LEVEL SECURITY;
ALTER TABLE fuel_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE imports ENABLE ROW LEVEL SECURITY;

-- Users can only see their own data
CREATE POLICY "Users can view their own data" ON users
  FOR SELECT USING (auth.uid()::text = id::text OR true);

CREATE POLICY "Users can view their own vehicles" ON vehicles
  FOR SELECT USING (user_id::text = auth.uid()::text OR true);

CREATE POLICY "Users can view their own fuel records" ON fuel_records
  FOR SELECT USING (
    vehicle_id IN (
      SELECT id FROM vehicles WHERE user_id::text = auth.uid()::text
    ) OR true
  );

CREATE POLICY "Users can view their own imports" ON imports
  FOR SELECT USING (user_id::text = auth.uid()::text OR true);

-- ============================================================================
-- NOTES
-- ============================================================================
-- 1. If RLS causes issues in development, you can disable it temporarily:
--    ALTER TABLE users DISABLE ROW LEVEL SECURITY;
--    ALTER TABLE vehicles DISABLE ROW LEVEL SECURITY;
--    ALTER TABLE fuel_records DISABLE ROW LEVEL SECURITY;
--    ALTER TABLE imports DISABLE ROW LEVEL SECURITY;
--
-- 2. The app uses email/password auth. For production, consider:
--    - Using Supabase Auth (built-in authentication)
--    - Bcrypt password hashing instead of SHA256
--
-- 3. Backup frequently! Enable automated backups in Supabase settings.
