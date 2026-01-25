import yagmail
import config
import logging
import resend
import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

import traceback

def send_email(subject, contents, attachments=None, inline_images=None, provider=None):
    """
    Send an email using Resend (priority) or QQ Mail (fallback).
    
    :param subject: Email subject
    :param contents: Email body (can be a list of text/html or a single string)
    :param attachments: List of file paths to attach
    :param inline_images: List of dicts {'path': str, 'cid': str} for inline images
    :param provider: 'resend' or 'qq'. If None, defaults to Resend with fallback.
    """
    
        # Determine provider priority
    use_resend = True
    if provider == 'qq':
        use_resend = False
    elif provider == 'resend':
        use_resend = True
    else:
        # Default behavior: Use Resend if key exists
        use_resend = bool(config.RESEND_API_KEY)

    # Validate QQ config if using QQ
    if not use_resend:
        if not config.QQ_EMAIL or not config.QQ_EMAIL_PASSWORD:
            logging.error("QQ Mail configuration missing (QQ_EMAIL or QQ_EMAIL_PASSWORD). Cannot send via QQ.")
            return False

    # 1. Try Resend First
    if use_resend and config.RESEND_API_KEY:
        for attempt in range(3): # Retry logic
            try:
                resend.api_key = config.RESEND_API_KEY
                
                # Handle contents (Resend expects a string for html)
                html_content = ""
                if isinstance(contents, list):
                    html_content = "".join([str(c) for c in contents if isinstance(c, str)])
                else:
                    html_content = str(contents)
                
                params = {
                    "from": "Twitter Monitor <onboarding@resend.dev>",
                    "to": config.RECEIVER_EMAIL,
                    "subject": subject,
                    "html": html_content,
                }
                
                # Handle attachments and inline images
                resend_attachments = []
                if attachments:
                    for file_path in attachments:
                        if os.path.exists(file_path):
                            with open(file_path, "rb") as f:
                                file_content = f.read()
                                resend_attachments.append({
                                    "filename": os.path.basename(file_path),
                                    "content": list(file_content)
                                })
                
                if inline_images:
                    for img in inline_images:
                        file_path = img['path']
                        cid = img['cid']
                        if os.path.exists(file_path):
                            with open(file_path, "rb") as f:
                                file_content = f.read()
                                resend_attachments.append({
                                    "filename": os.path.basename(file_path),
                                    "content": list(file_content),
                                    "content_id": cid
                                })
                
                if resend_attachments:
                    params["attachments"] = resend_attachments

                email = resend.Emails.send(params)
                logging.info(f"Email sent successfully via Resend: {email}")
                return True
            except Exception as e:
                logging.error(f"Attempt {attempt+1}/3 failed to send via Resend: {e}")
                time.sleep(1) # Wait before retry
        
        logging.error("All Resend attempts failed. Falling back to QQ Mail.")
        # Fall through to QQ Mail logic

    try:
        # If we have inline images, we should manually build the MIME message to support CID correctly
        # yagmail handles simple cases well, but for strict CID support matching Resend's logic, 
        # manual construction via smtplib is safer.
        if inline_images:
            logging.info("Using standard smtplib for QQ Mail (Inline Images Support)")
            
            # Create a multipart/related message (essential for inline images)
            msg = MIMEMultipart('related')
            msg['Subject'] = subject
            msg['From'] = f"News on Twitter <{config.QQ_EMAIL}>"
            msg['To'] = config.RECEIVER_EMAIL
            
            # Prepare HTML content
            html_content = ""
            if isinstance(contents, list):
                html_content = "".join([str(c) for c in contents if isinstance(c, str)])
            else:
                html_content = str(contents)
            
            # Attach HTML part
            msg.attach(MIMEText(html_content, 'html'))
            
            # Attach Inline Images
            for img in inline_images:
                file_path = img['path']
                cid = img['cid']
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        img_data = f.read()
                        image_part = MIMEImage(img_data)
                        image_part.add_header('Content-ID', f'<{cid}>') # Note the angle brackets
                        image_part.add_header('Content-Disposition', 'inline', filename=os.path.basename(file_path))
                        msg.attach(image_part)
            
            # Attach Regular Attachments
            if attachments:
                for file_path in attachments:
                     if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                            msg.attach(part)
            
            # Send via SMTP_SSL
            # with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
            #     server.login(config.QQ_EMAIL, config.QQ_EMAIL_PASSWORD)
            #     server.send_message(msg)
            
            # Use yagmail to handle connection/login robustness
            user_alias = {config.QQ_EMAIL: 'News on Twitter'}
            yag = yagmail.SMTP(user=user_alias, password=config.QQ_EMAIL_PASSWORD, host='smtp.qq.com')
            yag.login() # Ensure connected
            yag.smtp.send_message(msg)
            yag.close()
            
            logging.info(f"Email sent successfully (Standard SMTP via yagmail connection): {subject}")
            return True

        else:
            # Use yagmail for simple cases
            logging.info("Using yagmail for QQ Mail")
            
            # Prepare attachments for QQ Mail
            qq_attachments = attachments if attachments else []
            
            # Initialize yagmail
            user_alias = {config.QQ_EMAIL: 'News on Twitter'}
            yag = yagmail.SMTP(user=user_alias, password=config.QQ_EMAIL_PASSWORD, host='smtp.qq.com')
            
            # Send
            yag.send(
                to=config.RECEIVER_EMAIL,
                subject=subject,
                contents=contents,
                attachments=qq_attachments if qq_attachments else None
            )
            logging.info(f"Email sent successfully (yagmail): {subject}")
            return True
            
    except Exception as e:
        logging.error(f"Failed to send email via QQ: {e}")
        logging.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    print("Testing email sender...")
    # send_email("Test Subject", "This is a test body.")
