/*
	This is to copy the existing database into the new setup
*/

/* First we get the users */

truncate auth_users;
truncate swimmers_swimmers;
truncate registration_plans;
truncate registration_periods; 
truncate registration_payments;
truncate registration_registrations;
truncate registration_registrations_payments; 

insert into auth_users select a.iSwimmerID as id, 1 as is_active, a.szEmailAddress as username, \
	a.szFirstName as first_name, a.szLastName as last_name, a.szEmailAddress as email, '' as password, \
	0 as is_staff, 0 as is_superuser, NOW() as last_login, if(min(b.dRegDate) != '0000-00-00', \
	min(b.dRegDate), '2004-12-06') as date_joined from tblSwimmer as a, tblRegister as b \
	where a.iSwimmerID = b.iSwimmerID group by username;

/* this is to ensure I don't lock myself out of the database */

update auth_users set password = 'sha1$0f8b7$258cfbcd0f237f54fb80056469567df2bf526dd1', username = 'hal9000', \
	is_staff = 1, is_superuser = 1, last_login = NOW() where first_name = 'Frederick' and last_name = 'Grim';

/* Now we line up swimmers_swimmers */

insert into swimmers_swimmers ( user_id, street, street2, city, state_id, zipcode, usms_code, \
	date_of_birth, day_phone, evening_phone, gender ) select c.id, a.szStreetAddress1, \
	a.szStreetAddress2, a.szCity, b.id, a.szZipCode, a.szUSMSnum, a.dDOB, a.szDayPhone, \
	a.szEveningPhone, a.cGender from tblSwimmer as a, swimmers_states as b, auth_users as c where 
	a.szState = b.code and a.iSwimmerID = c.id;

insert into registration_plans ( id, name, base_amount, late_fee, description, reg_period_id, \
	swim_count, add_annual, isrecurring ) select iPlanID, szPlanDesc, fPlanAmount, \
	fLateFee, szPlanDesc, iPeriodID, iSwimCount, 0, 0 from tblPaymentPlan;

insert into registration_periods ( id, period_start, period_end ) select iPeriodID, dRegPeriodStart, \
	dRegPeriodEnd from tblRegistrationPeriod;

insert into registration_payments ( id, paypal_trans_id, swimmer_id, paid_date, amount_paid ) 
	select a.iPaymentID, a.szPaypalTxnID, b.id, a.dDatePaid, a.fAmountPaid \
	from tblPayment as a, swimmers_swimmers as b where a.iSwimmerID = b.user_id;

insert ignore into registration_registrations ( id, swimmer_id, registration_date, registration_status, plan_id, 
	comment ) select a.iRegisterID, b.id, if(a.dRegDate != '0000-00-00', a.dRegDate, a.dPaidDate), \
	a.iIsPaid, a.iPlanID, a.szComment from tblRegister as a, swimmers_swimmers as b where a.iSwimmerID = b.user_id;

insert into registration_registrations_payments ( registration_id, payment_id ) select a.iRegisterID as registration_id, b.iPaymentID as payment_id \
	from tblRegister as a, tblPayment as b where a.iSwimmerID = b.iSwimmerID and a.iPlanID = b.iPlanID \
	and a.iPeriodID = b.iPeriodID;

update auth_users as a, swimmers_swimmers as b, registration_registrations as c set a.is_active = 0 where 
	a.id = b.user_id and b.id = c.swimmer_id and ( c.registration_status = 0 or c.registration_status = 4 )

/*
drop table tblSwimmer;
drop table tblPaymentPlan;
drop table tblRegistrationPeriod;
drop table tblPayment;
drop table tblRegister;
*/
