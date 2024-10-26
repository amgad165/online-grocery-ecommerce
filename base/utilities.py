from django.core.mail import send_mail
from django.utils.html import format_html
from django.conf import settings
import locale
# # Set the locale to German (Austria)
# locale.setlocale(locale.LC_NUMERIC, 'de_AT.UTF-8')


def mail(order,sender, items_lists,user=None, kind=None):
    

    if kind == 'company_confirmation':
        message = format_html(
            f"Hallo sm-handels,<br><br>"
            f"Bitte überprüfen Sie die folgenden Angaben:<br><br>"
            f"• Vorname: {user.first_name}<br>"
            f"• Nachname: {user.last_name}<br>"
            f"• Firmenname: {user.company_name}<br>"
            f"• ATU-Nummer: {user.atu_number}<br>"
            f"• E-Mail: {user.email}<br>"
            f"• Bezirk: {user.bezirk}<br>"
            f"• Postleitzahl: {user.plz_zip}<br>"
            f"• Adresse: {user.street_address}<br>"
            f"• Hausnummer: {user.hausnummer}<br><br>"
            f"Es ist erforderlich, dass die ATU-Nummer überprüft wird, um sicherzustellen, dass sie korrekt und gültig ist.<br><br>"
            f"Beste Grüße,<br>"
            f"Team S&M Handels"
        )

        client_email = [user.email]

        send_mail(
            'Neue Kundenregistrierung – Überprüfung der ATU-Nummer erforderlich',
            message,
            from_email=sender,
            recipient_list=client_email,
            fail_silently=False,
            html_message=message
        )


    elif kind == 'order_without_price':

        message = format_html(
            f"Sehr geehrte/r {order.user.first_name}. <br><br>"
            f"wir freuen uns, Ihnen mitteilen zu können, dass Ihre Bestellung mit der Bestellnummer <strong>{order.id}</strong> erfolgreich eingegangen ist. Hier sind die Details Ihrer Bestellung:<br><br>"

            f"{items_lists}<br><br>"
            
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
            f"Ort: {order.user.bezirk}<br>"
            f"Adresse: {order.user.street_address}<br>"
            f"Hausnummer: {order.user.hausnummer}<br>"
            f"Postleitzahl: {order.user.plz_zip}<br><br>"

            f"Gesamtbestellung basierend auf dem System: {order.get_final_total()}€<br><br>"
            f"Anmerkung: Diese Bestellung ist eine Geschäftsbestellung ohne Preise, die an den Benutzer gesendet wird."
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


    else:
        


        message = format_html(
            f"Sehr geehrte/r {order.user.first_name}. <br><br>"
            f"wir freuen uns, Ihnen mitteilen zu können, dass Ihre Bestellung mit der Bestellnummer <strong>{order.id}</strong> erfolgreich eingegangen ist. Hier sind die Details Ihrer Bestellung:<br><br>"

            f"{items_lists}<br><br>"
            
            f"Gesamtbetrag: {order.get_final_total()}€<br><br>"

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
            f"Ort: {order.user.bezirk}<br>"
            f"Adresse: {order.user.street_address}<br>"
            f"Hausnummer: {order.user.hausnummer}<br>"
            f"Postleitzahl: {order.user.plz_zip}<br>"

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
