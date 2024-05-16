from django.core.mail import send_mail
from django.utils.html import format_html
from django.conf import settings
import locale
# # Set the locale to German (Austria)
# locale.setlocale(locale.LC_NUMERIC, 'de_AT.UTF-8')


def mail(order,sender, items_lists):
    



    message = format_html(
        f"Betreff: Bestellbestätigung für Ihre Bestellung {order.id} ,<br><br>"
        f"Sehr geehrte/r {order.user.first_name}. <br><br>"
        f"wir freuen uns, Ihnen mitteilen zu können, dass Ihre Bestellung mit der Bestellnummer <strong>{order.id}</strong> erfolgreich eingegangen ist. Hier sind die Details Ihrer Bestellung:<br><br>"

        f"{items_lists}<br><br>"
        
        f"Gesamtbetrag: {order.get_total()}€<br><br>"

        f"Wir bearbeiten Ihre Bestellung umgehend. Bei Fragen zu Ihrer Bestellung stehen wir Ihnen gerne zur Verfügung.<br><br>"
        f"Vielen Dank für Ihre Bestellung!<br><br>"
        f"Mit freundlichen Grüßen,<br>"
        f"Team S&M Handels"

    )

    client_email = [order.user.email]

    send_mail(
        'Deine Bestellung',
        message,
        from_email=sender,
        recipient_list=client_email,
        fail_silently=False,
        html_message=message
    )
    

    message = format_html(
        f"Bestellnummer: {order.id},<br><br>"
        f"<strong>Bestellte Gerichte:</strong> <br><br>"
        f"{items_lists} <br><br>"
        f"Kunden-E-Mail: {order.user.email}<br><br>"
        f"Telefonnummer des Kunden: {order.user.atu_number} <br><br>"
        f"bezirk: {order.user.bezirk}<br>"
        f"street_address: {order.user.street_address}<br>"
        f"hausnummer: {order.user.hausnummer}<br>"
        f"plz_zip: {order.user.plz_zip}<br>"

    )

    # Send email to bazroz mail
    send_mail(
        'Neue Bestellung',
        message,
        from_email=sender,
        recipient_list=[sender],
        fail_silently=False,
        html_message=message
    )
