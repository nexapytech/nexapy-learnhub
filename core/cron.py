from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    # Set schedule for the cron job, e.g., every 60 minutes
    RUN_EVERY_MINS = 60  # Every 60 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'  # Unique code for your cron job

    def do(self):
        # Logic to be executed periodically
        print("This is a cron job that runs every hour.")
