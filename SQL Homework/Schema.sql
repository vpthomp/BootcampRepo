CREATE TABLE Departments (
	Dept_no varchar(255),
	Dept_name varchar(255)
);
CREATE TABLE Dept_emp(
	Emp_no integer,
	Dept_no varchar(255),
	From_date date,
	To_date date
	);
CREATE TABLE Dept_manager(
	Dept_no varchar(255),
	Emp_no integer,
	From_date date,
	To_date date,
	PRIMARY KEY (Dept_no),
	FOREIGN KEY (Emp_no) REFERENCES Dept_emp(Emp_no)
);
CREATE TABLE Employees(
	Emp_no integer,
	Birth_date date,
	First_name varchar(255),
	Last_name varchar(255),
	Gender varchar(255),
	Hire_date date,
	PRIMARY KEY (Emp_no)
);
CREATE TABLE Salaries (
	Emp_no integer,
	Salary integer,
	From_date date,
	To_date date,
	PRIMARY KEY (Emp_no)
);
CREATE TABLE Titles (
	Emp_no integer,
	Title varchar(255),
	From_date date,
	To_date date
);
select * from departments;
select * from dept_emp;
select * from dept_manager;
select * from employees;
select * from salaries;
select * from titles;

