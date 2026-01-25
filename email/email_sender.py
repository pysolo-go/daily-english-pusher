import yagmail
import config
import logging

def send_email(subject, contents, attachments=None):
    """
    Send an email using QQ Mail.
    
    :param subject: Email subject
    :param contents: Email body (can be a list of text/html)
    :param attachments: List of file paths to attach
    """
    try:
        # Initialize yagmail with QQ credentials
        # Use a dictionary to set the sender alias (Display Name)
        # Format: { 'email_address': 'Display Name' }
        user_alias = {config.QQ_EMAIL: 'News on Twitter'}
        
        yag = yagmail.SMTP(user=user_alias, password=config.QQ_EMAIL_PASSWORD, host='smtp.qq.com')
        
        # Send the email
        yag.send(
            to=config.RECEIVER_EMAIL,
            subject=subject,
            contents=contents,
            attachments=attachments
        )
        logging.info(f"Email sent successfully: {subject}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False

if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    print("Testing email sender...")
    # send_email("Test Subject", "This is a test body.")
