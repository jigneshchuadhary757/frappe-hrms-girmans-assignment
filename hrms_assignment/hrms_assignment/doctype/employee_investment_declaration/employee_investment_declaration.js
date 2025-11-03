// Copyright (c) 2025, Jignesh Chaudhary and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Investment Declaration", {
	refresh(frm) {
		compute_total(frm);
	},

	section_80c(frm) {
		compute_total(frm);
	},

	section_80d(frm) {
		compute_total(frm);
	},

	other_exemptions(frm) {
		compute_total(frm);
	}
});

function compute_total(frm) {
	let total =
		(frm.doc.section_80c || 0) +
		(frm.doc.section_80d || 0) +
		(frm.doc.other_exemptions || 0);

	frm.set_value("total_investment", total);
}