# Imports the account management functionalities for initial accounts setup.
from accountManagement import submitRUApplication, approveRUApplication, \
                                denyRUApplication, banRegisteredUser

# Imports the product management functionalities for initial products setup.
from productManagement import submitProduct, approveProductListing, \
                                denyProductListing, banProductListing

# Imports the report management functionalities for initial reports setup.
from reportsManagement import submitReport, approveReport, denyReport

# Imports the admin dashboard functionalities for testing.
from admin_dashboard import getPendingApplicants, getRegisteredUsers, getDeniedUsers, getBannedUsers, \
                            getPendingProducts, getListedProducts, getDeniedProducts, getBannedProducts, \
                            getPendingReports, getApprovedReports, getDeniedReports

# Manually setups initial accounts for WeiBayLLC.
def setup_accounts():
    # Manually submits application for the regular users and administrators (WeiBayLLC owners).
    submitRUApplication('Andy', 'Zheng', 'Andy.Zheng@gmail.com', 'password', 'password', 'RUSER')
    submitRUApplication('Brailinson', 'Disla', 'Brailinson.Disla@gmail.com', 'password', 'password', 'ADMIN')
    submitRUApplication('Cristian', 'Statescu', 'Cristian.Statescu@gmail.com', 'password', 'password', 'RUSER')
    submitRUApplication('Manuel', 'Pohl', 'Manuel.Pohl@gmail.com', 'password', 'password', 'RUSER')
    submitRUApplication('Talike', 'Bennett', 'Talike.Bennett@gmail.com', 'password', 'password', 'RUSER')

    # Manually approve, deny, and band applications for the administrators.
    approveRUApplication('Andy.Zheng')
    approveRUApplication('Brailinson.Disla')
    approveRUApplication('Cristian.Statescu')
    denyRUApplication('Manuel.Pohl')
    approveRUApplication('Talike.Bennett')
    banRegisteredUser('Cristian.Statescu')

# Manually setups initial products for WeiBayLLC.
def setup_products():
    # Manually submits application for a few products.
    submitProduct(2, 'Water Bottles', 'This is a pack of bottled waters.', 'NEW', 100, 16.99)
    submitProduct(2, 'Juice Bottles', 'This is a pack of bottled juice.', 'NEW', 100, 19.99)
    submitProduct(1, 'Water Bottles', 'This is a pack of bottled waters.', 'USED', 100, 7.99)
    submitProduct(1, 'Water Boat', 'Brand new water boat.', 'NEW', 100, 16943.99)
    submitProduct(2, 'Burguer Pack', 'This is a pack of vegan burgers.', 'NEW', 100, 17.99)

    # Manually approve, deny and ban product listings.
    approveProductListing(2, 'Water Bottles')
    denyProductListing(2, 'Juice Bottles')
    approveProductListing(1, 'Water Bottles')
    approveProductListing(1, 'Water Boat')
    approveProductListing(2, 'Burger Pack')
    banProductListing(1, 'Water Boat')

# Manually setups initial reports for WeiBayLLC.
def setup_reports():
    # Manually submits reports.
    submitReport(1, 2, 1, "These water bottles are disgusting!")
    submitReport(1, 2, 5, "These water bottles are sweet!")
    submitReport(3, 1, 2, "These water bottles are swollen!")
    submitReport(3, 1, 5, "These water bottles are empty!")

    # Manually approve and deny product reports.
    approveReport(1, 2, 1)
    denyReport(1, 2, 5)
    approveReport(3, 1, 2)
    approveReport(3, 1, 5)

# Get user functionalities for admin dashboard.
def test_admin_dashboard():
    # Prints users pending approval.
    print("Users Pending Approval:")
    for user in getPendingApplicants():
        print('\t' + str(user))

    # Formatting.
    print("")

    # Prints registered users.
    print("Registered Users:")
    for user in getRegisteredUsers():
        print('\t' + str(user))

    # Formatting.
    print("")

    # Prints denied users.
    print("Denied Users:")
    for user in getDeniedUsers():
        print('\t' + str(user))

    # Formatting.
    print("")

    # Prints banned users.
    print("Banned Users:")
    for user in getBannedUsers():
        print('\t' + str(user))

    # Formatting.
    print("\n")

    # Prints the products pending approval.
    print("Products Pending Approval:")
    for product in getPendingProducts():
        print('\t' + str(product))

    # Formatting.
    print("")

    # Prints listed products.
    print("Listed Products:")
    for product in getListedProducts():
        print('\t' + str(product))

    # Formatting.
    print("")

    # Prints denied products.
    print("Denied Products:")
    for product in getDeniedProducts():
        print('\t' + str(product))

    # Formatting.
    print("")

    # Prints banned products.
    print("Banned Products:")
    for product in getBannedProducts():
        print('\t' + str(product))

    # Formatting.
    print("\n")

    # Prints pending reports.
    print("Pending Reports:")
    for report in getPendingReports():
        print('\t' + str(report))

    # Formatting.
    print("")

    # Prints approved reports.
    print("Approved Reports:")
    for report in getApprovedReports():
        print('\t' + str(report))

    # Formatting.
    print("")

    # Prints denied reports.
    print("Denied Reports:")
    for report in getDeniedReports():
        print('\t' + str(report))

    # Formatting.
    print("")
