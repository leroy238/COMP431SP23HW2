import sys

sys.stdout.write("MAIL FROM: <jeffay@cs.unc.edu>\n")
sys.stdout.write("RCPT TO: <bob@cs.unc.edu>\n")
sys.stdout.write("RCPT TO: <bob@cs.unc.edu>\n")
sys.stdout.write("RCPT TO: <bob@cs.unc.edu>\n")
sys.stdout.write("RCPT TO: <bob@cs.unc.edu>\n")
sys.stdout.write("DATA\n")
sys.stdout.write("The Simple Mail Transfer Protocol (SMTP) is an Internet standard communication protocol for electronic mail transmission. Mail servers and other message transfer agents use SMTP to send and receive mail messages. User-level email clients typically use SMTP only for sending messages to a mail server for relaying, and typically submit outgoing email to the mail server on port 587 or 465 per RFC 8314. \n")
sys.stdout.write("For retrieving messages, IMAP (which replaced the older POP3) is standard, but proprietary servers also often implement proprietary protocols, e.g., Exchange ActiveSync.\n")
sys.stdout.write(". \n")
sys.stdout.write(" \n")
sys.stdout.write("Message actually endes with a single period on a line by itself.\n")
sys.stdout.write(".\n")