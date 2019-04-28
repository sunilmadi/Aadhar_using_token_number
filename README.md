# Aadhar_using_token_number_option-4
Generate aadhar number using the token number and pancard combination. And insert the generated aadhar number to aadhar database and send sms and email to user.
1) Take pancard number and token number from user.
2) Using pannum and token number and TOEKN_USED='N' , hit the TOKEN table. if record doesnt exists, '0' is returned along with error message "INVALID TOKEN/PANCARD COMBINATION" and stop processing/
3) if record exists in TOKEN table, hit PANCARD table using input pannumber and if no record exits, throw error and stop processing.
4) if record exists in PANCARD table, hit AADHARINFO collection using aadhar number fetched from PANCARD table. If document exists in AADHARINFO collection, send the aadhar details to sms/email to user.
If document doesnt exists in AADHARINFO collection, insert details into AADHARINFO collection and send sms/email to user.Update entry in TOKEN table with TOEKN_USED='Y'
