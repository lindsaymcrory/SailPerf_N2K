
CREATE TABLE IF NOT EXISTS gps_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
    );

CREATE TABLE wind_log (
    id INTEGER PRIMARY KEY,
    timestamp TEXT NOT NULL,
    wind_speed REAL,
    wind_angle REAL
);

CREATE TABLE boat_speed_log (
    id INTEGER PRIMARY KEY,
    timestamp TEXT NOT NULL,
    boat_speed REAL
);

CREATE TABLE tracks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,  -- Local system timestamp in ISO format
    gpgll_time NUMERIC,       -- Time from GPGLL sentence
    latitude NUMERIC,         -- GPS latitude in decimal degrees
    longitude NUMERIC,        -- GPS longitude in decimal degrees
    heading_true NUMERIC,     -- True heading (degrees)
    heading_mag NUMERIC,      -- Magnetic heading (degrees)
    boat_speed_nm NUMERIC,    -- Boat speed in nautical miles per hour
    wind_speed_true_nm NUMERIC,  -- True wind speed (knots)
    wind_dir_ref TEXT,        -- Wind direction reference (T = true, R = relative)
    wind_speed_apparent_nm NUMERIC -- Apparent wind speed (knots)
);