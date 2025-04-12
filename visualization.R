# Install necessary packages if not already installed
packages <- c("DBI", "RSQLite", "gt", "dplyr", "ggplot2", "viridis", "gridExtra")

# Check and install missing packages
new_packages <- packages[!(packages %in% installed.packages()[,"Package"])]
if(length(new_packages)) install.packages(new_packages)

# Load necessary libraries
library(DBI)
library(RSQLite)
library(gt)
library(dplyr)
library(ggplot2)
library(viridis)
library(gridExtra)

# Specify the file path of the SQLite database
file_path <- "electronic_parts.db"  # Replace this with the actual file path

# Create a directory to save outputs
if (!dir.exists("output")) {
  dir.create("output")
}

# Connect to the SQLite database
conn <- dbConnect(RSQLite::SQLite(), file_path)

# List all tables in the database
tables <- dbListTables(conn)
if (!"Parts" %in% tables) {
  stop("The 'Parts' table does not exist in the database.")
}

# Query data from the Prices table, selecting the convertedPrice column
price <- dbGetQuery(conn, "SELECT date, quantity, convertedPrice AS price, company_name FROM Prices where mpn = 'A000066'")

# Removes repetitions and include multiple dates
price_unique <- price %>%
  distinct(date, company_name, .keep_all = TRUE) %>%  # Ensure unique rows for each company on each date
  group_by(date) %>%  # Group by date
  slice_head(n = 4) %>%  # Takes the top 3 rows for each date
  ungroup() %>%
  arrange(date, company_name)  # Sort by date and company name

# Arrange the price data in descending order for each date
price_sorted <- price_unique %>%
  arrange(date, desc(price))  # Sort by date, then by price in descending order

# Select the first 10 entries for display
price_subset <- price %>%
  arrange(date, company_name) %>%  # Sort by date and company name
  head(10)  # Select the first 10 rows

# Display the first 10 rows of Price table and save as HTML
price_table_1 <- price_subset %>%
  gt() %>%
  tab_header(
    title = "Prices Table",
    subtitle = "Displaying 10 unique entries for each company"
  ) %>%
  fmt_date(
    columns = vars(date),  # Format the date column
    date_style = 3  # Medium style (e.g., Jan 7, 2025)
  ) %>%
  cols_label(
    date = "Date",
    quantity = "Quantity",
    price = "Price (Euros)",
    company_name = "Company Name"
  )

# Save the table as an HTML file
gtsave(price_table_1, "output/price_table_1.html")

# Display the sorted Price table and save as HTML
price_table_2 <- price_sorted %>%
  gt() %>%
  tab_header(
    title = "Prices Table",
    subtitle = "Displaying unique entries for each company, sorted by descending prices for each date"
  ) %>%
  fmt_date(
    columns = vars(date),  # Format the date column
    date_style = 3  # Medium style (e.g., Jan 7, 2025)
  ) %>%
  fmt_number(
    columns = vars(price),  # Format the price column
    decimals = 2  # Two decimal places for prices
  ) %>%
  cols_label(
    date = "Date",
    quantity = "Quantity",
    price = "Price (Euros)",
    company_name = "Company Name"
  ) %>%
  opt_row_striping()

# Save the table as an HTML file
gtsave(price_table_2, "output/price_table_2.html")

# Query the 'Parts' table
parts_data <- dbGetQuery(conn, "SELECT * FROM Parts where mpn = 'A000066'")

# Ensure the table is not empty
if (nrow(parts_data) == 0) {
  stop("The 'Parts' table is empty. Cannot create a table view.")
}

# Creates a formatted Parts table and save as HTML
parts_table <- parts_data %>%
  gt() %>%
  tab_header(
    title = "Parts Table",
    subtitle = "Displaying all columns from the Parts table"
  ) %>%
  cols_label(
    part_id = "Part ID",
    part_name = "Part Name",
    manufacturer_name = "Manufacturer Name",
    manufacturer_id = "Manufacturer ID"
  )

# Save the table as an HTML file
gtsave(parts_table, "output/parts_table.html")

# Query the 'Availability' table
availability_data <- dbGetQuery(conn, "SELECT * FROM Availabilty where mpn = 'A000066'")

# Removes true duplicates based on `date` and `total_availability`
availability_data <- availability_data %>%
  group_by(date, total_availability) %>%
  slice(1) %>%  # Retain only the first occurrence
  ungroup()

# Displays the 'Availability' table and save as HTML
availability_table <- availability_data %>%
  gt() %>%
  tab_header(
    title = "Availability Table",
    subtitle = "Displaying rows for Total availability per date"
  ) %>%
  cols_label(
    id = "ID",
    date = "Date",
    total_availability = "Total Availability",
    mpn = "MPN"
  ) %>%
  fmt_date(
    columns = vars(date),  # Format the date column
    date_style = 3  # Medium date style (e.g., Jan 7, 2025)
  ) %>%
  fmt_number(
    columns = vars(total_availability),  # Format the Total Availability column
    decimals = 0  # No decimal places for total availability
  ) %>%
  tab_style(
    style = cell_text(weight = "bold"),  # Bold column headers
    locations = cells_column_labels(everything())
  )

# Save the table as an HTML file
gtsave(availability_table, "output/availability_table.html")

# Disconnect from the database
dbDisconnect(conn)

# Reconnect to the database for further analysis and visualization
conn <- dbConnect(RSQLite::SQLite(), file_path)

# Query the Prices table for relevant columns
query_prices <- "SELECT date, quantity, convertedPrice AS price, company_name FROM Prices where mpn = 'A000066'"
data_prices <- dbGetQuery(conn, query_prices)

# Ensure date is in proper date format
data_prices$date <- as.Date(data_prices$date)

# Query data from the Availability table and aggregate total availability by date
avail_data <- dbGetQuery(conn, "SELECT date, total_availability 
                               FROM Availabilty where mpn = 'A000066'
                               GROUP BY date 
                               ORDER BY date")

# Disconnect from the database again
dbDisconnect(conn)

# Convert the 'date' column in availability data to Date type for proper plotting
avail_data$date <- as.Date(avail_data$date)

# Extract year and month for faceting
avail_data$year <- format(avail_data$date, "%Y")

# Get 21 distinct colors using the viridis color scale
colors <- viridis(21)  # Create exactly 21 colors

# Create a function to generate the plot for each page
generate_plot <- function(companies_data, colors) {
  max_price <- max(companies_data$price, na.rm = TRUE)  # Get the maximum price to set y-axis limit
  
  ggplot(companies_data, aes(x = date, y = price, color = company_name)) +
    geom_point() +  # Use dots to represent prices
    facet_grid(rows = vars(quantity), cols = vars(company_name)) +  # Facet by quantity and company
    scale_color_manual(values = colors) +  # Apply distinct colors
    labs(title = "Price Variation with Respect to Time for Each Quantity and Company",
         x = "Date",
         y = "Price") +
    ylim(0, max_price) +  # Set y-axis range from 0 to max price
    theme_bw() +  # Use a white background theme
    theme(
      axis.text.x = element_text(angle = 90, hjust = 1),  # Rotate date labels vertically
      legend.position = "none",  # Remove the legend (company name) from the right side
      panel.background = element_rect(fill = "white"),  # Ensure the panel background is white
      plot.background = element_rect(fill = "white"),  # Ensure the plot background is white
      strip.background = element_rect(fill = "white")  # Ensure the facet strip background is white
    )
}

# Split the companies into three groups
unique_companies <- unique(data_prices$company_name)

# Divide the companies into 3 pages, each containing 7 companies
companies_page_1 <- unique_companies[1:7]
companies_page_2 <- unique_companies[8:14]
companies_page_3 <- unique_companies[15:21]

# Filter the data for each page's companies
data_page_1 <- data_prices[data_prices$company_name %in% companies_page_1, ]
data_page_2 <- data_prices[data_prices$company_name %in% companies_page_2, ]
data_page_3 <- data_prices[data_prices$company_name %in% companies_page_3, ]

# Generate plots for each page
plot_page_1 <- generate_plot(data_page_1, colors[1:7])
plot_page_2 <- generate_plot(data_page_2, colors[8:14])
plot_page_3 <- generate_plot(data_page_3, colors[15:21])

# Save the plots as PNG files with a white background
ggsave("output/plot_page_1.png", plot_page_1, width = 10, height = 6, bg = "white")
ggsave("output/plot_page_2.png", plot_page_2, width = 10, height = 6, bg = "white")
ggsave("output/plot_page_3.png", plot_page_3, width = 10, height = 6, bg = "white")

# Plotting the dot graph (scatter plot) for total availability over time, faceted by year
availability_plot <- ggplot(avail_data, aes(x=date, y=total_availability)) +
  geom_point(color="steelblue", size=2) +  # Dot plot instead of bar
  geom_smooth(method="loess", se=FALSE, color="red", linetype="dashed") +  # Trend line
  labs(title="Total Availability vs Time",  # Updated title
       x="Date",
       y="Total Availability") +
  theme_bw() +  # Use a white background theme
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),  # Rotate date labels for better readability
    plot.title = element_text(hjust = 0.5),  # Center title
    panel.background = element_rect(fill = "white"),  # Ensure the panel background is white
    plot.background = element_rect(fill = "white"),  # Ensure the plot background is white
    strip.background = element_rect(fill = "white")  # Ensure the facet strip background is white
  ) +
  facet_wrap(~ year, scales = "free_x")  # Facet by year

# Save the availability plot as a PNG file with a white background
ggsave("output/availability_plot.png", availability_plot, width = 10, height = 6, bg = "white")

# Disconnect from the database
dbDisconnect(conn)