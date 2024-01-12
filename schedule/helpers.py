# from . import views
#
# from django.core.mail import EmailMessage
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import icalendar
# from datetime import datetime, timedelta
# #
# #
# # def send_calendar_invite(subject, body, start_time, end_time, recipient_email):
# #
# #         # Create a multipart message
# #         msg = MIMEMultipart()
# #
# #         # Add email headers
# #         msg['Subject'] = subject
# #         msg['From'] = 'your_email@example.com'
# #         msg['To'] = recipient_email
# #         msg['Date'] = formatdate(localtime=True)
# #
# #         # Create the iCalendar (.ics) content
# #         calendar_content = f"""BEGIN:VCALENDAR
# #             VERSION:2.0
# #             BEGIN:VEVENT
# #             SUMMARY:{subject}
# #             DESCRIPTION:{body}
# #             DTSTART;TZID=America/New_York:{start_time}
# #             DTEND;TZID=America/New_York:{end_time}
# #             ORGANIZER:your_email@example.com
# #             LOCATION:Meeting Room
# #             STATUS:CONFIRMED
# #             SEQUENCE:0
# #             BEGIN:VALARM
# #             TRIGGER:-PT10M
# #             DESCRIPTION:Reminder
# #             ACTION:DISPLAY
# #             END:VALARM
# #             END:VEVENT
# #             END:VCALENDAR
# #             """
# #
# #         # Attach the iCalendar file
# #         calendar_attachment = MIMEText(calendar_content, 'calendar;method=REQUEST')
# #         calendar_attachment.add_header('Content-Disposition', 'attachment', filename='invite.ics')
# #         msg.attach(calendar_attachment)
# #
# #         # Send the email
# #         with EmailMessage() as email:
# #             email.subject = subject
# #             email.body = body
# #             email.from_email = 'your_email@example.com'
# #             email.to = [recipient_email]
# #             email.attach_file('path/to/your/logo.png')  # You can attach files if needed
# #             email.attach(msg.as_string(), 'message/rfc822')  # Attach the multipart message
# #
# #             # Send the email
# #             email.send()
# #
# #     # Example usage
# #     subject = 'Meeting Invitation'
# #     body = 'Please join our meeting.'
# #     start_time = '20240115T120000'  # Replace with the actual start time in the format 'YYYYMMDDTHHMMSS'
# #     end_time = '20240115T130000'    # Replace with the actual end time in the format 'YYYYMMDDTHHMMSS'
# #     recipient_email = 'recipient@example.com'
# #
# #     send_calendar_invite(subject, body, start_time, end_time, recipient_email)
# #
# def send_email_with_ics(subject, body, startDate, endDate, email):
#     # Create an event in iCalendar format
#     cal = icalendar.Calendar()
#     event = icalendar.Event()
#
#     event.add('summary', 'Meeting')
#     event.add('dtstart', startDate)
#     event.add('dtend', endDate)
#     cal.add_component(event)
#
#     ics_content = cal.to_ical()
#
#     # Create an email message
#     subject = str(subject)
#     body = str(body)
#     from_email = 'your_email@example.com'
#     to_email = str(email)
#
#     msg = MIMEMultipart()
#     msg['Subject'] = subject
#     msg['From'] = from_email
#     msg['To'] = to_email
#     msg.attach(MIMEText(body))
#
#     # Attach the ICS file
#     attachment = MIMEText(ics_content, 'calendar; method=REQUEST')
#     attachment.add_header('Content-Disposition', 'attachment', filename='meeting.ics')
#     msg.attach(attachment)
#
#     # Send the email
#     email = EmailMessage(subject, body, from_email, [to_email])
#     email.attach_alternative(body, 'text/plain')
#     email.attach('meeting.ics', ics_content, 'text/calendar')
#     email.send()
#
#     return HttpResponse('Email sent successfully!')
