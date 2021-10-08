import db_utils
import sys
import os

#Insert Records into Tables
def insert_records(ibotta, files_location):
    #list of tables in db
    table_names = ['customer_offer_redemptions', 'customer_offer_rewards', 'customer_offers', 'offer_rewards']
    file_names = os.listdir(files_location)
    for file, table in zip(file_names, table_names):
        file_name = r"C:\Users\User\Desktop\ibotta\CSV_data\{0}".format(file)
        #calling loadcsv in db_utils package
        db_utils.loadcsv(ibotta, file_name, table)

def query_for_questions(ibotta,output_files):
    query1 = "SELECT CUSTOMER_ID,count(1) as count_of_offer_activations from customer_offers cor where ACTIVATED != '' group by 1 order by count_of_offer_activations desc"
    query2 = "SELECT DISTINCT CUSTOMER_ID FROM customer_offers co where ACTIVATED < DATE('now','-2 months')"
    query3 = """with cte as (SELECT CUSTOMER_ID ,COUNT(ACTIVATED ) as ACTIVATED_count from customer_offers where ACTIVATED != '' group by CUSTOMER_ID  ),
cte1 as (SELECT CUSTOMER_ID , count(VERIFIED ) as VERIFIED_count from customer_offers co where VERIFIED != '' group by CUSTOMER_ID )
SELECT cte.customer_id, (cte1.verified_count*1.0/cte.activated_count)*100 as conversion_rate from cte join cte1 on cte.customer_id = cte1.customer_id order by conversion_rate"""
    query4 = "select co.CUSTOMER_ID ,sum(OFFER_AMOUNT ) as amount from customer_offer_redemptions cor join customer_offers co on cor.CUSTOMER_OFFER_ID =co.ID group by co.CUSTOMER_ID order by 2 desc"
    list_q = [query1,query2,query3,query4]
    c = 1
    #writing the output to txt files.
    for query in list_q:
        location = output_files + "\query" + str(c)+".txt"
        results = [db_utils.db_query(ibotta, query)]
        file = open(location,'w' )
        file.writelines(str(results))
        c+=1



def main(argv):
    # specify the path location for ibotta.db
    ibotta = db_utils.create_connection(argv[1])  # specify the path location for ibotta.db
    files_location = argv[2]
    #inserting the records
    #insert_records(ibotta, files_location)
    #specify the path for output location
    output_files = argv[3]
    #query the db
    query_for_questions(ibotta,output_files)



# run mainv
if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise Exception('Incorrect number of arguments passed')
    main(sys.argv[:])
