# HID Usage Tables Source Identity Selection Checklist

> Status: checklist only
> Authority ceiling: source_identity_selection_checklist_only

This packet defines the source identity fields that must be selected before a
future Level 3 HID Usage Tables source-authority import. It does not select the
publication identity and does not enable Usage Tables citation authority.

## Source Candidate

- source_id: `hid_usage_tables`
- current status: `not_imported`
- selected publication identity: `TBD_LEVEL3_APPROVAL`

## Required Identity Fields

- publisher
- document_title
- publication_version_or_revision
- publication_date
- canonical_url
- imported_scope
- excluded_scope

## Required Review Questions

- Does the selected source identity match the document being imported?
- Is the imported scope narrow enough for the first source-authority slice?
- Is the excluded scope explicit enough to prevent report payload or parser
  claims?
- Are citation and source-registry updates in the same checkpoint?

## Non-Claims

- no selected publication identity in this packet
- no source authority import in this packet
- no Usage Tables citation authority in this packet
- no Usage Tables governed entries in this packet
