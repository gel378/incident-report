# -*- coding: utf-8 -*-
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "incident_report.db"

SEED_DATA = [
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS001","SYSTEM * AcuPick * Order stuck in In Progress - Missing PICKUP Activity"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS002","SYSTEM * AcuPick * Order stuck in In Progress - Missing DROP_OFF Activity"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS003","SYSTEM * AcuPick * Order stuck in In Progress - DROP_OFF Activity Stuck in RELEASED"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS004","SYSTEM * AcuPick * Order stuck in In Progress - Cancelled activity"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS005","SYSTEM * AcuPick * Order stuck in In Progress - Cancelled PICK_PACK activity"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS006","SYSTEM * AcuPick * Order stuck in In Progress - Cancelled DROP_OFF activity"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS007","SYSTEM * AcuPick * Order stuck in In Progress - Cancelled PICKUP activity"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS008","SYSTEM * AcuPick * Order stuck in In Progress - Picklist Prep Not Ready status"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS009","SYSTEM * AcuPick * Order stuck in Pending Release "),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS010","SYSTEM * AcuPick * Not receiving arrival notification on picking device"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS011","SYSTEM * AcuPick * PPD Connection Issue"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS012","SYSTEM * AcuPick * PPD Connection Issue - \"Something Went Wrong\""),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS013","SYSTEM * AcuPick * PPD Scanning Issue - Unable to Scan All Items"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS014","SYSTEM * AcuPick * PPD Scanning Issue - Unable to Scan Specific Items"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS015","SYSTEM * AcuPick * PPD Scanning Issue - \"Wrong Item Scanned\""),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS016","SYSTEM * AcuPick * PPD Scanning Issue - \"No Item Scanned\""),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS017","SYSTEM * AcuPick * PPD Scanning Issue - \"Error Computing Quantity\""),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS018","SYSTEM * AcuPick * PPD Scanning Issue - Weight‑based items not scanning correctly"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS019","SYSTEM * AcuPick * Resolve Exception status in Acupick but Pickup Ready in DTILL"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS020","SYSTEM * AcuPick * Picklist shows Zero Item Qty"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS021","SYSTEM * AcuPick * Unreleased Orders"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS022","SYSTEM * AcuPick * Picked order still shows Ready to Pick in Acupick "),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS023","SYSTEM * AcuPick * Unable to stage order - API Response Error Message \" NULL\""),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS024","SYSTEM * AcuPick * Unable to stage order - API Response Error Message \"Not all quantity got picked\""),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS025","SYSTEM * AcuPick * App crashes whenever Tote Count is Less Than Order Count for a Rolling Batch Picklist"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS026","SYSTEM * AcuPick * Chat assist will not display shop assist messages"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS027","SYSTEM * AcuPick * Timer keeps on running after handoff"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS028","SYSTEM * AcuPick * Handoff timer triggered before arrival / Ghost notification"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS029","SYSTEM * AcuPick * Not receiving FLASH order drop notification"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS030","SYSTEM * AcuPick * Incorrect item description"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS031","SYSTEM * AcuPick * Missing Order"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS032","SYSTEM * AcuPick * Incorrect item image in picklist"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS033","SYSTEM * AcuPick * Unable to access tote labels to print"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS034","SYSTEM * AcuPick * Bag Label Reprinting Issue"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS035","SYSTEM * AcuPick * Acupick is Down"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS036","SYSTEM * AcuPick * Order stage time is incorrect"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS037","SYSTEM * AcuPick * Error printing labels - config issue"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS038","SYSTEM * AcuPick * Pre-pick order - Preplist Notification Issue"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS039","SYSTEM * AcuPick * Login Issue - Network Error / \"An error occurred. Please try again\""),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS040","SYSTEM * AcuPick * Mapping Issue"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS041","SYSTEM * AcuPick * Timer starting off on negative count"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS042","SYSTEM * AcuPick * Order Duplicate Picklists issue "),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS043","SYSTEM * AcuPick * RX Orders Showing Zero Items in PPD"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS044","SYSTEM * AcuPick * RX Order Handoff Issue"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS045","SYSTEM * AcuPick * Not receiving Express order drop notification"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS046","SYSTEM * AcuPick * App version is not updated"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS047","SYSTEM * AcuPick * AcuPick App is missing in PPD"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS048","SYSTEM * AcuPick * No picklists generated for Ready to Pick orders"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS049","SYSTEM * AcuPick * Reshop/Prep Not Ready issue"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS050","SYSTEM * AcuPick * Produce items are not scanning forcing picker to perform substitution"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS051","SYSTEM * AcuPick * No notification of customer rejected substitution"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS052","SYSTEM * AcuPick * Customer did not receive the Substitution Notification - Unable to Approve/Reject"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS053","SYSTEM * AcuPick * Unable to \"Mark as Arrived\" in PPD"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS054","SYSTEM * AcuPick * Acupick app stops when doing substitution"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS055","SYSTEM * AcuPick * Items in order automatically go out of stock"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS056","SYSTEM * AcuPick * Incorrect item zone"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS057","SYSTEM * AcuPick * PPDs not receiving notifications when new orders come in"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS058","SYSTEM * AcuPick * Order Staging - keeps on asking bag/loose count after scanning bag labels"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS059","SYSTEM * AcuPick * items should be sold by quantity, not weight or vice versa"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS060","SYSTEM * AcuPick * Order not flowing to DTILL - stuck in \"Staging Complete\" in Acupick"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS061","SYSTEM * AcuPick * No order arrival received - \"Error loading data. There was a error loading arrivals data\" on Acupick"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS062","SYSTEM * AcuPick * Staging - Duplicate Key Error"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS063","SYSTEM * AcuPick * Unable to substitute, \"complete\" box is missing"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS064","SYSTEM * AcuPick * \"Incorrect Item\" error during picking"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS065","SYSTEM * AcuPick * Order Handoff - \"This order is already assigned to another associate\""),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS066","SYSTEM * AcuPick * Handoff stucked : \"Do you want to begin or continue staging?\""),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS067","SYSTEM * AcuPick * No Order Details in Dashboard due to Duplicate lineID"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS068","SYSTEM * AcuPick * Timer is not running"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS069","SYSTEM * AcuPick * \"Item not available\" error when picking"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS070","SYSTEM * AcuPick * Multiplying the qty/weight of produce items"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS071","SYSTEM * AcuPick * Preplist Duplicate Printing  "),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS072","SYSTEM * AcuPick * Scanning specific item crashes the AcuPick app"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS073","SYSTEM * AcuPick * Pick quantity is greater than remaining quantity error"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS074","SYSTEM * AcuPick * Order Stuck in \"Picked Up – Payment Requested\" Status"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS075","SYSTEM * AcuPick * Orders at risk are not highlighted as Red/Pink"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS076","SYSTEM * AcuPick * No handoff timer for 3PL order"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS077","SYSTEM * AcuPick * Missing item images/descriptions in picklist"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS078","SYSTEM * AcuPick * Deli item error - \"Amount enter is too heavy, check with department\""),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS079","SYSTEM * AcuPick * substituting produce - \"select quantity\" button not working"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS080","SYSTEM * AcuPick * Staging Issue - printing labels for a diff customer"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS081","SYSTEM * AcuPick * Kept on asking valid ID for non-regulated items"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS082","SYSTEM * AcuPick * Order generating extra bag tags"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS083","SYSTEM * AcuPick * \"Verify code\" button disappear when Store enter a wrong auth code first time"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS084","SYSTEM * AcuPick * Negative picked qty"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS085","SYSTEM * AcuPick * Order has an alcohol but not prompting for Age verification "),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS086","SYSTEM * AcuPick * Preplist is not Printing"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS087","SYSTEM * AcuPick * Missing Items in Preplist"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS088","SYSTEM * AcuPick * Reschedule link is not working"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS089","SYSTEM * AcuPick * ESL not lighting up when using Pick‑to‑Light feature on handhelds"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS090","SYSTEM * AcuPick * Tote issue - Not enough capacity for batched orders"),
    ("SYSTEM","eCom Picking Mgmt. System (OSPK)","OSPKSYS091","SYSTEM * AcuPick * Unreleased Orders - Stuck in Coming Up status"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS001","OPS * AcuPick * Store reports they can't complete/stage order but order is complete"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS002","OPS * AcuPick * Label Printing Issue"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS003","OPS * AcuPick * Training Issue - Order Handoff - Order Stuck in Pickup Ready"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS004","OPS * AcuPick * Training Issue - Staging an Order"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS005","OPS * AcuPick * Store inquiry about past orders"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS006","OPS * AcuPick * Store inquiry about today's orders"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS007","OPS * AcuPick * Store inquiry on cancelled order"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS008","OPS * AcuPick * Order Cancellation Request"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS009","OPS * AcuPick * Resolve Exception status in Acupick – waiting for store to process fixable VPOS exception"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS010","OPS * AcuPick * Acupick dashboard is not responding/loading"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS011","OPS * AcuPick * Store is not yet done picking the order - Pending completion of Picklist"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS012","OPS * AcuPick * Unable to confirm pickup of order"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS013","OPS * AcuPick * Existing picker in Acupick is unable to login"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS014","OPS * AcuPick * Add/Update Account Request"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS015","OPS * AcuPick * Training Issue - Dynamic Batch Orders showing Ready to Pick"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS016","OPS * AcuPick * Training Issue - Dynamic Batch Orders showing Coming Up"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS017","OPS * AcuPick * Switch Label Printer"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS018","OPS * AcuPick * Training issue - Reassign picklist"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS019","OPS * AcuPick * Store Inquires if order is charged"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS020","OPS * AcuPick * Store reports order is not in DTILL but it is there when checked"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS021","OPS * AcuPick * Training issue - Scanning item"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS022","OPS * AcuPick * Awaiting Customer Response – waiting for the customer to approved subbed items"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS023","OPS * AcuPick * Store inquiry about a future order"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS024","OPS * AcuPick * orders dropping randomly instead of in a sequence"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS025","OPS * AcuPick * Request to change order type"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS026","OPS * AcuPick * Produce Scale Issue"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS027","OPS * AcuPick * Inquiry for splitting order into mutiple picklists"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS028","OPS * AcuPick * Deployment - orders are not dropping to AcuPick"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS029","OPS * AcuPick * Store Inquires if there are orders for the day"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS030","OPS * AcuPick * Store is using incorrect AcuPick dashboard link"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS031","OPS * AcuPick * User accidentally logged in to other store and is now unable to take out the order"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS032","OPS * AcuPick * Training Issue - Order Drop Schedule"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS033","OPS * AcuPick * Early order drop in PPD"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS034","OPS * AcuPick * Store request to edit items on today's order"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS035","OPS * AcuPick * Password Reset"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS036","OPS * AcuPick * Inquiry on item missing in receipt but item substitution was rejected"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS037","OPS * AcuPick * Training Issue - incorrect picked qty"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS038","OPS * AcuPick * Store request to reschedule the order"),
    ("OPS","eCom Picking Mgmt. System (OSPK)","OSPKOPS039","OPS * AcuPick * Remove/Add Item to Catalog Request"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS001","SYSTEM * VPOS * TILLING_EXCEPTION: Key details are missing from the order. Please create an incident with IT. - Missing Item Price"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS002","SYSTEM * VPOS * TILLING_EXCEPTION: Key details are missing from the order. Please create an incident with IT. - Missing Customer Name"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS003","SYSTEM * VPOS * TILLING_EXCEPTION: Key details are missing from the order. Please create an incident with IT. - Missing Extended Price"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS004","SYSTEM * VPOS * TILLING_EXCEPTION: Key details are missing from the order. Please create an incident with IT. - Missing Customer Address"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS005","SYSTEM * VPOS * TILLING_EXCEPTION: Key details are missing from the order. Please create an incident with IT. - Missing PaymentSubType"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS006","SYSTEM * VPOS * POS_SYSTEM_ERROR - POSBC Initialization Failed"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS007","SYSTEM * VPOS * SYSTEM_INTERNAL_ERROR - Unexpected Exception occurred while processing the order"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS008","SYSTEM * VPOS * SYSTEM_INTERNAL_ERROR - Refund"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS009","SYSTEM * VPOS * SYSTEM_INTERNAL_ERROR: PEPE Service Internal Error"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS010","SYSTEM * VPOS * PRICING_EXCEPTION - Unable to fix the exception"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS011","SYSTEM * VPOS * Controlled Item Limit"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS012","SYSTEM * VPOS * PAYMENT_DECLINE Exception - app issue"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS013","SYSTEM * VPOS * Departmental item is not eligible for fix"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS014","SYSTEM * VPOS * POS_DISPLAY_TEXT - refund"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS015","SYSTEM * VPOS * POS_SYSTEM_ERROR - Refund"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS016","SYSTEM * VPOS * Receipt Not Printing"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS017","SYSTEM * VPOS * Orders Not Processing in PSBR App"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS018","SYSTEM * VPOS * PEPE_ORDER_SAVINGS_ERROR - Order Savings not applied. To be reprocessed."),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS019","SYSTEM * VPOS * DTILL Stuck in Running Status - Refund issue"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS020","SYSTEM * VPOS * VPOS is Down"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS021","SYSTEM * VPOS * Unable to refund recently completed orders in VPOS"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS022","SYSTEM * VPOS * JSON PARSING ERROR"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS023","SYSTEM * VPOS * Blank Exception"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS024","SYSTEM * VPOS * POS_DISPLAY_TEXT Exception"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS025","SYSTEM * VPOS * TILLING EXCEPTION - Order with restricted item alcohol - not automatically reprocessed after restriction time"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS026","SYSTEM * VPOS * DTILL Exception B034 Error Processing Tender Override Item"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS027","SYSTEM * VPOS * Switch store receipt printer"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS028","SYSTEM * VPOS * Item cannot legally be sold(Incorrect UPC)"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS029","SYSTEM * VPOS * Page cannot be displayed"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS030","SYSTEM * VPOS * Orders stuck in \"Ready\" status - CSS & services restart"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS031","SYSTEM * VPOS * Regulated form not printing"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS032","SYSTEM * VPOS * Ecom/Shopsite Customers Not Receiving J4U Discount (Missed Discount)"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS033","SYSTEM * VPOS * PRICING_EXCEPTION - No item description "),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS034","SYSTEM * VPOS * Item Not Found - Item Description is \"No Description\""),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS035","SYSTEM * VPOS * DTILL Stuck in Running Status"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS036","SYSTEM * VPOS * DTILL Stuck in Running - css restart"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS037","SYSTEM * VPOS * Multiple orders stuck in processing - missing config"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS038","SYSTEM * VPOS * Orders Not Flowing to DTILL - Kafka Internal Server Error"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS039","SYSTEM * VPOS * Incorrect server time - Item cannot legally be sold exception"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS040","SYSTEM * VPOS * Minimum order fee $3.95 was charged to customer"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS041","SYSTEM * VPOS * Unable to process SNAP Tenders"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS042","SYSTEM * VPOS * Looping/Repeating Weight & Quantity Value in Fixit"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS043","SYSTEM * VPOS * Session Not Available (Connection Status: DISCONNECTED): AddTender"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS044","SYSTEM * VPOS * Service POSBC is DOWN"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS045","SYSTEM * VPOS * Payment Exception: Unable to process a refund"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS046","SYSTEM * VPOS * Service VPOSACE is DOWN"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS047","SYSTEM * VPOS * POS application not in state to perform start transaction "),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS048","SYSTEM * VPOS * Invalid Key Sequence"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS049","SYSTEM * VPOS * incorrect Bag fee setup"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS050","SYSTEM * VPOS * Missing/Incomplete Items in an Order"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS051","SYSTEM * VPOS * Incorrect Exception Time in DTILL"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS052","SYSTEM * VPOS * JSON PARSING ERROR - Error while parsing order items,String index out of range: 3"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS053","SYSTEM * VPOS * Incorrect item descriptions in PDF Digital Receipts but not in RPT"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS054","SYSTEM * VPOS * VPOS Stopped - service stopped"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS055","SYSTEM * VPOS * Invalid Club card number"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSSYS056","SYSTEM * VPOS * Error Applying POS Tender"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSPAY001","SYSTEM * VPOS * Payment Exception - Please create an incident with IT - No declined payment record in OCSE/OSPG DB"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSPAY002","SYSTEM * VPOS * Payment Exception - Please create an incident with IT - EBT refund after FF success; CC Declined"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSPAY003","SYSTEM * VPOS * PAYMENT_EXCEPTION - Please create an incident with IT - Declined Paypal"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSPAY004","SYSTEM * VPOS * PAYMENT_EXCEPTION - Please create an incident with IT - BannerCash Issue"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSPAY005","SYSTEM * VPOS * Payment Exception - Please create an incident with IT - EBT refund after FF success; Paypal Declined"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSPAY006","SYSTEM * VPOS * Payment Exception - Please create an incident with IT - EBT refund after FF failed; CC success"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSPAY007","SYSTEM * VPOS * PAYMENT EXCEPTION - Technical Error Message: 400 BAD_REQUEST"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSPAY008","SYSTEM * VPOS* PAYMENT_EXCEPTION - Please create an incident with IT - Declined Charge in Direct Spend"),
    ("SYSTEM","VPOS - Virtual Point of Sale System (OSVP)","VPOSPAY009","SYSTEM * VPOS* PAYMENT_EXCEPTION - Please create an incident with IT - Declined Charge in ApplePay"),
    ("OPS","VPOS - Virtual Point of Sale System (OSVP)","VPOSOPS001","OPS * VPOS * Refund Request"),
    ("OPS","VPOS - Virtual Point of Sale System (OSVP)","VPOSOPS002","OPS * VPOS * Item Not Found – Training on how to fix the exception"),
    ("OPS","VPOS - Virtual Point of Sale System (OSVP)","VPOSOPS003","OPS * VPOS * Item cannot legally be sold exception - order contains alcohol"),
    ("OPS","VPOS - Virtual Point of Sale System (OSVP)","VPOSOPS004","OPS * VPOS * Refund receipt not printing"),
    ("OPS","VPOS - Virtual Point of Sale System (OSVP)","VPOSOPS005","OPS * VPOS * Unable to login to Refund page"),
    ("OPS","VPOS - Virtual Point of Sale System (OSVP)","VPOSOPS006","OPS * VPOS * Item cannot legally be sold exception(Recalled Item)"),
    ("OPS","VPOS - Virtual Point of Sale System (OSVP)","VPOSOPS007","OPS * VPOS * PAYMENT_DECLINE Exception - declined card"),
    ("OPS","VPOS - Virtual Point of Sale System (OSVP)","VPOSOPS008","OPS * VPOS * PRICING_EXCEPTION - Training on how to fix the exception"),
    ("OPS","VPOS - Virtual Point of Sale System (OSVP)","VPOSOPS009","OPS * VPOS * Remove order in exception from DTILL request"),
    ("OPS","VPOS - Virtual Point of Sale System (OSVP)","VPOSOPS010","OPS * VPOS * Clear print queue job request"),
    ("OPS","VPOS - Virtual Point of Sale System (OSVP)","VPOSOPS011","OPS * VPOS * Store Inquiry on order in PICKUP READY in DTILL"),
    ("OPS","VPOS - Virtual Point of Sale System (OSVP)","VPOSOPS012","OPS * VPOS * Manual charging request"),
    ("OPS","VPOS - Virtual Point of Sale System (OSVP)","VPOSOPS013","OPS * VPOS * Tilling Exception - order contains alcohol"),
    ("OPS","VPOS - Virtual Point of Sale System (OSVP)","VPOSOPS014","OPS * VPOS * Store inquiry on DTILL UI Login"),
    ("SYSTEM","eCommerce Order Mgmt. System (for Micro Fulfillment Center) (OSCO)","OSCOSYS001","SYSTEM * OSCO * Order not flowing to DTILL - Stuck in PACKED due to Large Order"),
    ("SYSTEM","eCommerce Order Mgmt. System (for Micro Fulfillment Center) (OSCO)","OSCOSYS002","SYSTEM * OSCO * Order not flowing to DTILL - PICK_START in OSCO - Stuck in In Progress; Activities are Complete in AcuPick"),
    ("SYSTEM","eCommerce Order Mgmt. System (for Micro Fulfillment Center) (OSCO)","OSCOSYS003","SYSTEM * OSCO * Order not flowing to DTILL - already in Payment Requested in OSCO"),
    ("SYSTEM","eCommerce Order Mgmt. System (for Micro Fulfillment Center) (OSCO)","OSCOSYS004","SYSTEM * OSCO * Order not flowing to DTILL - Stuck in PACKED and In Progress in Acupick (Complete FulfilledUPC) - with FAS error"),
    ("SYSTEM","eCommerce Order Mgmt. System (for Micro Fulfillment Center) (OSCO)","OSCOSYS005","SYSTEM * OSCO * Order not flowing to DTILL - Stuck in Pending Payment Status in Acupick"),
    ("SYSTEM","eCommerce Order Mgmt. System (for Micro Fulfillment Center) (OSCO)","OSCOSYS006","SYSTEM * OSCO * Order in Pickup ready status is not flowing to DTILL - Released in OSCO"),
    ("SYSTEM","eCommerce Order Mgmt. System (for Micro Fulfillment Center) (OSCO)","OSCOSYS007","SYSTEM * OSCO * Order not flowing to DTILL - stuck in Packed in OSCO"),
    ("SYSTEM","eCommerce Order Mgmt. System (for Micro Fulfillment Center) (OSCO)","OSCOSYS008","SYSTEM * OSCO * Order not flowing to DTILL - stuck in PRICED in OSCO"),
    ("SYSTEM","eCommerce Order Mgmt. System (for Micro Fulfillment Center) (OSCO)","OSCOSYS009","SYSTEM * OSCO * Order not flowing to DTILL - Stuck in STAGED status in OSCO"),
    ("SYSTEM","eCommerce Order Mgmt. System (for Micro Fulfillment Center) (OSCO)","OSCOSYS010","SYSTEM * OSCO * Order not flowing to DTILL - stuck in PICKED_UP in OSCO"),
    ("SYSTEM","eCommerce Order Mgmt. System (for Micro Fulfillment Center) (OSCO)","OSCOSYS011","SYSTEM * OSCO * Overcharged order (OSCO sending 'qty' as '1' as part of pricing request for the OOS items with upc starting with '02')"),
    ("SYSTEM","eCom Online Shopping Last Mile (OSLM)","OSLMSYS001","SYSTEM * OSLM * Order not flowing to Doordash / Uber"),
    ("SYSTEM","eCom Online Shopping Last Mile (OSLM)","OSLMSYS002","SYSTEM * OSLM * The PA notification chimes not going off at customers check in/arrival"),
    ("SYSTEM","eCom Online Shopping Last Mile (OSLM)","OSLMSYS003","SYSTEM * OSLM * 3PL Portal is not loading"),
    ("SYSTEM","eCom Online Shopping Last Mile (OSLM)","OSLMSYS004","SYSTEM * OSLM * Unable to login to Doordash"),
    ("SYSTEM","eCom Online Shopping Last Mile (OSLM)","OSLMSYS005","SYSTEM * OSLM * Multiple drivers being dispatched for the same order"),
    ("SYSTEM","eCom Online Shopping Last Mile (OSLM)","OSLMSYS006","SYSTEM * OSLM * No Available Flash Slots"),
    ("SYSTEM","eCom Online Shopping Last Mile (OSLM)","OSLMSYS007","SYSTEM * OSLM * Spotlight TV is not Accessible"),
    ("OPS","eCom Online Shopping Last Mile (OSLM)","OSLMOPS001","OPS * 3PL * Store Request for Redelivery in Last Mile UI"),
    ("OPS","eCom Online Shopping Last Mile (OSLM)","OSLMOPS002","OPS * 3PL * Store Request for Cancellation of Delivery in Last Mile UI"),
    ("OPS","eCom Online Shopping Last Mile (OSLM)","OSLMOPS003","OPS * 3PL * Store Associate unable to login in Last Mile UI Link"),
    ("SYSTEM","Salesforce Marketing Cloud (EMSF)","EMSFSYS001","SYSTEM * EMSF * Customer unable to check in on App"),
    ("OPS","Salesforce Marketing Cloud (EMSF)","EMSFOPS001","OPS * EMSF * DUG Phones not receive notification when customer presses ON THE WAY from the app"),
    ("SYSTEM","Descartes Route Planner (OSRP)","OSRPSYS001","SYSTEM * OSRP * Cancelled order - Order Release Failure"),
    ("SYSTEM","Descartes Route Planner (OSRP)","OSRPSYS002","SYSTEM * OSRP * Cancelled orders are not flowing to RP from EOM correctly"),
    ("SYSTEM","Descartes Route Planner (OSRP)","OSRPSYS003","SYSTEM * OSRP * Duplicate order in Van Trip Summary"),
    ("SYSTEM","Descartes Route Planner (OSRP)","OSRPSYS004","SYSTEM * OSRP * Early Van Allocation "),
    ("SYSTEM","Descartes Route Planner (OSRP)","OSRPSYS005","SYSTEM * OSRP * Incorrect Van Departure Time"),
    ("SYSTEM","Descartes Route Planner (OSRP)","OSRPSYS006","SYSTEM * OSRP * Missing vans for multiple stores"),
    ("SYSTEM","Descartes Route Planner (OSRP)","OSRPSYS007","SYSTEM * OSRP * missing in RP"),
    ("SYSTEM","Descartes Route Planner (OSRP)","OSRPSYS008","SYSTEM * OSRP * Optimization issue -too much orders in 1 van"),
    ("SYSTEM","Descartes Route Planner (OSRP)","OSRPSYS009","SYSTEM * OSRP * Order not in AVL"),
    ("SYSTEM","Descartes Route Planner (OSRP)","OSRPSYS010","SYSTEM * OSRP * Orders not dropping (RP issue)"),
    ("SYSTEM","Descartes Route Planner (OSRP)","OSRPSYS011","SYSTEM * OSRP * RouteInfoUpdate - ABORTED"),
    ("SYSTEM","Descartes Route Planner (OSRP)","OSRPSYS012","SYSTEM * OSRP * RP DB logs full"),
    ("SYSTEM","Descartes Route Planner (OSRP)","OSRPSYS013","SYSTEM * OSRP * Stuck in Review"),
    ("SYSTEM","Descartes Route Planner (OSRP)","OSRPSYS014","SYSTEM * OSRP * scheduler configuration issue"),
    ("SYSTEM","Descartes Route Planner (OSRP)","OSRPSYS015","SYSTEM * OSRP * UI failed to load"),
    ("SYSTEM","Descartes Route Planner (OSRP)","OSRPSYS016","SYSTEM * OSRP * Unwaved Orders (DST Change)"),
    ("SYSTEM","Online Shopping Demand Planning (OSDP)","OSDPSYS001","SYSTEM * OSDP * Customer can't see slot capacity"),
    ("SYSTEM","Online Shopping Demand Planning (OSDP)","OSDPSYS002","SYSTEM * OSDP * Unable to access eCom Operations App"),
    ("SYSTEM","Online Shopping Demand Planning (OSDP)","OSDPSYS003","SYSTEM * OSDP * Store zipcode is mapped to different store"),
    ("OPS","Online Shopping Demand Planning (OSDP)","OSDPOPS001","OPS * OSDP * Store Slot Inquiry"),
    ("OPS","Online Shopping Demand Planning (OSDP)","OSDPOPS002","OPS * OSDP * Store Request for Slot Closure"),
    ("OPS","eCom Customer Order - Control Tower (OSCT)","OSCTOPS001","OPS * Control Tower * Site is showing  404 Not Found -  Order is showing no record found"),
]


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tracking_ref (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                type          TEXT NOT NULL,
                ci            TEXT NOT NULL,
                tracking_code TEXT NOT NULL UNIQUE,
                category      TEXT NOT NULL
            )
        """)
        # Always sync SEED_DATA — insert new codes, skip existing ones
        clean = [
            (t, ci, code, cat)
            for t, ci, code, cat in SEED_DATA
            if code and code.strip()
        ]
        conn.executemany(
            "INSERT OR REPLACE INTO tracking_ref (type, ci, tracking_code, category) VALUES (?,?,?,?)",
            clean
        )
        conn.commit()


def get_all_tracking() -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, type, ci, tracking_code, category FROM tracking_ref ORDER BY ci, tracking_code"
        ).fetchall()
    return [dict(r) for r in rows]


def upsert_tracking(id: int | None, type_: str, ci: str, tracking_code: str, category: str) -> dict:
    with get_conn() as conn:
        if id:
            conn.execute(
                "UPDATE tracking_ref SET type=?, ci=?, tracking_code=?, category=? WHERE id=?",
                (type_, ci, tracking_code, category, id)
            )
        else:
            conn.execute(
                "INSERT INTO tracking_ref (type, ci, tracking_code, category) VALUES (?,?,?,?)",
                (type_, ci, tracking_code, category)
            )
        conn.commit()
        row = conn.execute(
            "SELECT id, type, ci, tracking_code, category FROM tracking_ref WHERE tracking_code=?",
            (tracking_code,)
        ).fetchone()
    return dict(row)


def delete_tracking(id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM tracking_ref WHERE id=?", (id,))
        conn.commit()


def get_tracking_map() -> dict:
    rows = get_all_tracking()
    return {r["tracking_code"]: r for r in rows}


def get_ci_type_map() -> dict:
    rows = get_all_tracking()
    return {r["ci"]: r["type"] for r in rows}