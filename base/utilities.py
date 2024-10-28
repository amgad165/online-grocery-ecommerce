from django.core.mail import send_mail
from django.utils.html import format_html
from django.conf import settings
import locale
# # Set the locale to German (Austria)
# locale.setlocale(locale.LC_NUMERIC, 'de_AT.UTF-8')


def mail(order,sender, items_lists,user=None, kind=None):
    
    if order.user.address_type == "billing":
        user_address = f"{order.user.street_address} {order.user.hausnummer}, {order.user.plz_zip} {order.user.bezirk}"
        phone_number = order.user.atu_number
    else:
        user_address = str(order.user.delivery_addresses)
        phone_number = order.user.delivery_addresses.phone_number

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


        # Create the rest of the message content
        message = format_html(
            f"Sehr geehrte/r {order.user.first_name} {order.user.last_name}. <br><br>"
            f"<strong>Datum:</strong><br> {order.ordered_date.strftime('%d.%m.%Y')}<br><hr>"

            # Single Table for Alignment
            f"<table style='width: 100%; margin-top: 10px; border-collapse: collapse;'>"
            
            # Bestellnummer and Kundennummer Row
            f"<tr>"
            f"    <td style='font-weight: bold; width: 50%;'>Bestellnummer:</td>"
            f"    <td style='font-weight: bold;'>Kundennummer:</td>"
            f"</tr>"
            f"<tr>"
            f"    <td>{order.order_code}</td>"
            f"    <td>Nicht vorhanden</td>"
            f"</tr>"
            
            # Divider Row
            f"<tr><td colspan='2'><hr></td></tr>"
            
            # Bestellt von and Lieferadresse Row
            f"<tr>"
            f"    <td style='font-weight: bold;'>Bestellt von:</td>"
            f"    <td style='font-weight: bold;'>Lieferadresse:</td>"
            f"</tr>"
            f"<tr>"
            f"    <td>{order.user.first_name} ({phone_number})</td>"
            f"    <td>{user_address}</td>"
            f"</tr>"
            
            f"</table><hr>"

            f"<h3>Bestellübersicht:</h3><br>"
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
            f"Bestellnummer: {order.order_code},<br><br>"
            f"<strong>Bestellte Gerichte:</strong> <br><br>"
            f"{items_lists} <br><br>"
            f"Kunden-E-Mail: {order.user.email}<br><br>"
            f"Telefonnummer des Kunden: {phone_number} <br><br>"

            f"Adresse: {user_address}<br>"


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
            f"Sehr geehrte/r {order.user.first_name} {order.user.last_name}. <br><br>"
            f"<strong>Datum:</strong><br> {order.ordered_date.strftime('%d.%m.%Y')}<br><hr>"

            # Single Table for Alignment
            f"<table style='width: 100%; margin-top: 10px; border-collapse: collapse;'>"
            
            # Bestellnummer and Kundennummer Row
            f"<tr>"
            f"    <td style='font-weight: bold; width: 50%;'>Bestellnummer:</td>"
            f"    <td style='font-weight: bold;'>Kundennummer:</td>"
            f"</tr>"
            f"<tr>"
            f"    <td>{order.order_code}</td>"
            f"    <td>Nicht vorhanden</td>"
            f"</tr>"
            
            # Divider Row
            f"<tr><td colspan='2'><hr></td></tr>"
            
            # Bestellt von and Lieferadresse Row
            f"<tr>"
            f"    <td style='font-weight: bold;'>Bestellt von:</td>"
            f"    <td style='font-weight: bold;'>Lieferadresse:</td>"
            f"</tr>"
            f"<tr>"
            f"    <td>{order.user.first_name} ({phone_number})</td>"
            f"    <td>{user_address}</td>"
            f"</tr>"
            
            f"</table><hr>"

            f"<h3>Bestellübersicht:</h3><br>"
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
            f"Bestellnummer: {order.order_code},<br><br>"
            f"<strong>Bestellte Gerichte:</strong> <br><br>"
            f"{items_lists} <br><br>"
            f"Kunden-E-Mail: {order.user.email}<br><br>"
            f"Telefonnummer des Kunden: {phone_number} <br><br>"
            f"Adresse: {user_address}<br>"


        )

        # Send email to frischverliebt mail
        send_mail(
            'Neue Bestellung',
            message,
            from_email=sender,
            recipient_list=[sender],
            fail_silently=False,
            html_message=message
        )
