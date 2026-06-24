# Verification Status

## Summary

Source authority status: locked.

| Area | Tracked entries | Verified | Reviewed | Inferred | Missing |
|---|---:|---:|---:|---:|---:|
| HID descriptors | 7 | 1 | 6 | 0 | 0 |
| HID report descriptors | 6 | 1 | 5 | 0 | 0 |
| HID class requests | 6 | 6 | 0 | 0 | 0 |
| Report / boot / idle semantics | 0 | 0 | 0 | 0 | 0 |
| **Total** | **19** | **8** | **11** | **0** | **0** |

## Current Surface Summary

| Area | Tracked entries | Source |
|---|---:|---|
| HID descriptors | 7 | `data/hid_descriptor_fields_matrix.yaml` |
| HID report descriptors | 6 | `data/hid_report_descriptor_items_matrix.yaml` |
| HID class requests | 6 | `data/hid_class_request_matrix.yaml` |

## Source Authority Summary

| Authority area | Status |
|---|---|
| Primary source | HID 1.11 PDF registered |
| Current imported usage | Section 7.2 Class-Specific Requests, Section 6.2.1 HID Descriptor, and Section 6.2.2 Report Descriptor item types |
| HID Usage Tables | not imported |
| HID over I2C | excluded |
| OS input stack behavior | excluded |
| Firmware handler correctness | excluded |

## Evidence Packet Summary

| Artifact type | Count | Status |
|---|---:|---|
| Entry verification packets | 0 | Not introduced |

## Non-claims

- This page does not claim HID content is complete.
- This page explicitly tracks six verified HID class request entries (`GET_REPORT`, `SET_REPORT`, `GET_IDLE`, `SET_IDLE`, `GET_PROTOCOL`, `SET_PROTOCOL`)
  and does not claim any firmware implementation truth.
- This page does not claim any governed table is complete.
- This page does not claim firmware implementation truth.
- This page does not claim HID Usage Tables are imported.
- This page does not claim HID descriptor parser behavior.
