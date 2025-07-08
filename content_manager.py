# Install Gradio (frontend interface)
!pip install gradio --quiet

import gradio as gr
import json
import os
import re

# Setup File
db_file = "contacts.json"
if not os.path.exists(db_file):
    with open(db_file, "w") as f:
        json.dump([], f)

def load_contacts():
    with open(db_file, "r") as f:
        return json.load(f)

def save_contacts(data):
    with open(db_file, "w") as f:
        json.dump(data, f, indent=4)

# Validation Functions
def is_valid_email(email): return re.match(r"[^@]+@[^@]+\.[^@]+", email)
def is_valid_phone(phone): return re.fullmatch(r"\d{10}", phone) and len(set(phone)) != 1
def is_valid_name(name): return re.fullmatch(r"[A-Za-z]{3,}", name) is not None
def is_valid_lastname(name): return re.fullmatch(r"[A-Za-z]+", name) is not None

# Field Validators
def validate_fname(name, skip): return "" if skip else ("❌ Required." if not name else "✅" if is_valid_name(name) else "❌ Min 3 letters.")
def validate_lname(name, skip): return "" if skip else ("❌ Required." if not name else "✅" if is_valid_lastname(name) else "❌ Alphabets only.")
def validate_address(addr, skip): return "" if skip else ("❌ Required." if not addr else "✅")
def validate_email(email, skip): return "" if skip else ("❌ Required." if not email else "✅" if is_valid_email(email) else "❌ Invalid.")
def validate_phone(phone, skip): return "" if skip else ("❌ Required." if not phone else "✅" if is_valid_phone(phone) else "❌ 10 digits only.")

# Create Contact
def create_contact(fname, mname, lname, addr, email, phone):
    if not all([fname, lname, addr, email, phone]):
        return "⚠️ All required fields are needed.", fname, mname, lname, addr, email, phone, "", "", "", "", "", False
    if not is_valid_name(fname):
        return "❌ Invalid first name.", fname, mname, lname, addr, email, phone, "", "", "", "", "", False
    if not is_valid_lastname(lname):
        return "❌ Invalid last name.", fname, mname, lname, addr, email, phone, "", "", "", "", "", False
    if not is_valid_email(email):
        return "❌ Invalid email format.", fname, mname, lname, addr, email, phone, "", "", "", "", "", False
    if not is_valid_phone(phone):
        return "❌ Phone must be 10 digits.", fname, mname, lname, addr, email, phone, "", "", "", "", "", False

    contacts = load_contacts()
    for c in contacts:
        if c["email"] == email: return "⚠️ Email exists.", fname, mname, lname, addr, email, phone, "", "", "", "", "", False
        if c["phone"] == phone: return "⚠️ Phone exists.", fname, mname, lname, addr, email, phone, "", "", "", "", "", False

    contact = {
        "id": len(contacts) + 1,
        "first_name": fname,
        "middle_name": mname,
        "last_name": lname,
        "address": addr,
        "email": email,
        "phone": phone
    }
    contacts.append(contact)
    save_contacts(contacts)
    return f"✅ Contact created. Your ID is: {contact['id']}", "", "", "", "", "", "", "", "", "", "", "", True

# Update Contact (partial allowed)
def update_contact(cid, fname, mname, lname, addr, email, phone):
    contacts = load_contacts()
    for c in contacts:
        if c["id"] == int(cid):
            if fname and not is_valid_name(fname): return "❌ Invalid first name.", fname, mname, lname, addr, email, phone, "", "", "", "", "", False
            if lname and not is_valid_lastname(lname): return "❌ Invalid last name.", fname, mname, lname, addr, email, phone, "", "", "", "", "", False
            if email and not is_valid_email(email): return "❌ Invalid email.", fname, mname, lname, addr, email, phone, "", "", "", "", "", False
            if phone and not is_valid_phone(phone): return "❌ Invalid phone.", fname, mname, lname, addr, email, phone, "", "", "", "", "", False

            for other in contacts:
                if other["id"] != int(cid):
                    if email and other["email"] == email:
                        return "⚠️ Email already exists.", fname, mname, lname, addr, email, phone, "", "", "", "", "", False
                    if phone and other["phone"] == phone:
                        return "⚠️ Phone exists.", fname, mname, lname, addr, email, phone, "", "", "", "", "", False

            if fname: c["first_name"] = fname
            if mname: c["middle_name"] = mname
            if lname: c["last_name"] = lname
            if addr: c["address"] = addr
            if email: c["email"] = email
            if phone: c["phone"] = phone
            save_contacts(contacts)
            return "✅ Contact updated.", "", "", "", "", "", "", "", "", "", "", "", True
    return "❌ ID not found.", fname, mname, lname, addr, email, phone, "", "", "", "", "", False

# Delete Contact
def delete_contact(cid):
    contacts = load_contacts()
    new_contacts = [c for c in contacts if c["id"] != int(cid)]
    if len(new_contacts) == len(contacts):
        return "❌ Contact ID not found."
    save_contacts(new_contacts)
    return "✅ Contact deleted."

# Read Contacts
def read_contacts():
    contacts = load_contacts()
    if not contacts: return "No contacts."
    return "\n".join([f"{c['id']}. {c['first_name']} {c.get('middle_name', '')} {c['last_name']} | {c['email']} | {c['phone']} | {c['address']}" for c in contacts])

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## 📇 Contact Manager")
    skip_flag = gr.State(value=False)

    with gr.Tab("Create"):
        fname = gr.Textbox(label="First Name", placeholder="e.g. Hemalatha")
        mname = gr.Textbox(label="Middle Name (Optional)")
        lname = gr.Textbox(label="Last Name", placeholder="Initial")
        addr = gr.Textbox(label="Address", placeholder="Address")
        email = gr.Textbox(label="Email", placeholder="e.g. hemi@gmail.com")
        phone = gr.Textbox(label="Phone", placeholder="10 digit number")
        fname_msg = gr.Markdown()
        lname_msg = gr.Markdown()
        addr_msg = gr.Markdown()
        email_msg = gr.Markdown()
        phone_msg = gr.Markdown()
        fname.change(validate_fname, [fname, skip_flag], fname_msg)
        lname.change(validate_lname, [lname, skip_flag], lname_msg)
        addr.change(validate_address, [addr, skip_flag], addr_msg)
        email.change(validate_email, [email, skip_flag], email_msg)
        phone.change(validate_phone, [phone, skip_flag], phone_msg)
        out_create = gr.Markdown()
        gr.Button("Create Contact").click(
            create_contact,
            [fname, mname, lname, addr, email, phone],
            [out_create, fname, mname, lname, addr, email, phone, fname_msg, lname_msg, addr_msg, email_msg, phone_msg, skip_flag]
        )

    with gr.Tab("Update"):
        cid = gr.Number(label="Contact ID")
        ufname = gr.Textbox(label="First Name")
        umname = gr.Textbox(label="Middle Name")
        ulname = gr.Textbox(label="Last Name")
        uaddr = gr.Textbox(label="Address")
        uemail = gr.Textbox(label="Email")
        uphone = gr.Textbox(label="Phone")
        ufname_msg = gr.Markdown()
        ulname_msg = gr.Markdown()
        uaddr_msg = gr.Markdown()
        uemail_msg = gr.Markdown()
        uphone_msg = gr.Markdown()
        ufname.change(validate_fname, [ufname, skip_flag], ufname_msg)
        ulname.change(validate_lname, [ulname, skip_flag], ulname_msg)
        uaddr.change(validate_address, [uaddr, skip_flag], uaddr_msg)
        uemail.change(validate_email, [uemail, skip_flag], uemail_msg)
        uphone.change(validate_phone, [uphone, skip_flag], uphone_msg)
        out_update = gr.Markdown()
        gr.Button("Update Contact").click(
            update_contact,
            [cid, ufname, umname, ulname, uaddr, uemail, uphone],
            [out_update, ufname, umname, ulname, uaddr, uemail, uphone, ufname_msg, ulname_msg, uaddr_msg, uemail_msg, uphone_msg, skip_flag]
        )

    with gr.Tab("Read"):
        out_read = gr.Textbox(label="All Contacts", lines=10, interactive=False)
        gr.Button("Show All").click(read_contacts, outputs=out_read)

    with gr.Tab("Delete"):
        del_id = gr.Number(label="Contact ID to Delete")
        out_del = gr.Markdown()
        gr.Button("Delete Contact").click(delete_contact, inputs=del_id, outputs=out_del)

demo.launch(share=True, debug=True)
