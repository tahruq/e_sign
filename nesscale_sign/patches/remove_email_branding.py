# Copyright (c) 2026, Nesscale Solutions Pvt Ltd and contributors
# For license information, please see license.txt
"""Remove the shipped brand wrappers from existing signing email templates."""

import frappe

from nesscale_sign.email.seed import TEMPLATE_NAMES

# Match only the original shipped wrappers; preserve edited message bodies,
# subjects, and unrelated Email Template records.
_BRAND_HEADER = """	<div style="padding:20px 0 16px;border-bottom:1px solid #e5e7eb;">
		<span style="font-size:17px;font-weight:700;color:#2563eb;">{{ brand }}</span>
	</div>
"""
_BRAND_FOOTER = "This is an automated message from {{ brand }}."
_NEUTRAL_FOOTER = "This is an automated document signing notification."


def execute():
	for name in TEMPLATE_NAMES.values():
		if not frappe.db.exists("Email Template", name):
			continue
		doc = frappe.get_doc("Email Template", name)
		changed = False
		for field in ("response", "response_html"):
			original = doc.get(field)
			if not original:
				continue
			updated = original.replace(_BRAND_HEADER, "").replace(_BRAND_FOOTER, _NEUTRAL_FOOTER)
			if updated != original:
				doc.set(field, updated)
				changed = True
		if changed:
			doc.save(ignore_permissions=True)
