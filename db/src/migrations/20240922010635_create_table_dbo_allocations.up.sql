CREATE TABLE IF NOT EXISTS dbo.dim_allocations (
  allocation_id INT PRIMARY KEY,
  name VARCHAR(100),
  type VARCHAR(50)
);
