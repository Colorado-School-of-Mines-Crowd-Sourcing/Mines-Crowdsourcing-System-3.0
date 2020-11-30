from django.core.management.base import BaseCommand, CommandError
from participant.models import Task, User, Transaction
from django.core import mail
from django.core.mail import EmailMessage
import xlsxwriter

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.pay_users()
        self.redeem_user_balances()
        #email = EmailMessage(
        #    subject='Mines Crowdsourcing System Payments',
        #    body='Body',
        #    from_email='minescrowdsourcing@gmail.com',
        #    to=['maxgawason@gmail.com',],
        #)
        print("sending email")
        #email.attach_file('./temp/UserBalances.xlsx')
        #email.attach_file('./temp/TaskBalances.xlsx')
        #email.send(False) 
        print("finished sending email")

    def pay_users(self):
        tasks = Task.objects.all()
        task_payment_book = xlsxwriter.Workbook('./temp/TaskBalances.xlsx')
        task_payment_sheet = task_payment_book.add_worksheet()
        task_payment_sheet.write(0, 0, "User CWID")
        task_payment_sheet.write(0, 1, "Payment Index")
        task_payment_sheet.write(0, 2, "Reward Amount")
        row = 1
        for task in tasks:
            users_to_be_paid = task.approved_participants.all()
            for user in users_to_be_paid:
                    task_payment_sheet.write(row, 0, user.CWID)
                    task_payment_sheet.write(row, 1, task.payment_index)
                    task_payment_sheet.write(row, 2, task.reward_amount)
                    task.paid_participants.add(user)
                    task.approved_participants.remove(user)
                    row += 1
        task_payment_book.close()
        

    def redeem_user_balances(self):
        user_balances_to_be_redeemed = Transaction.objects.filter(processed=0)
        balance_book = xlsxwriter.Workbook('./temp/UserBalances.xlsx')
        balance_sheet = balance_book.add_worksheet()
        balance_sheet.write(0, 0, "Student CWID")
        balance_sheet.write(0, 1, "Balance Redeemed")
        row = 1
        for balance in user_balances_to_be_redeemed:
            print("balances")
            print(balance.recipient.CWID)
            balance_sheet.write(row, 0, balance.recipient.CWID)
            balance_sheet.write(row, 1, balance.amount)
            balance.processed = 1
            row += 1 
        balance_book.close()
