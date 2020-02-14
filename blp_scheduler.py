import schedule
import blp_potwierdzenia_wczoraj

schedule.every().day.at("14:20").do(blp_potwierdzenia_wczoraj.potwierdzenia_wczoraj)

#TODO po przeniesieniu na docelowy komp trzeba poprawić ścieżki do:
#TODO chromdiver
#TODO folder do pobiearania potwierdzeń przed przenisieniem do folderu docelowego

while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)
