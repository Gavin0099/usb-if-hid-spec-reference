# USB HID Spec Reference

本 repo 是 USB HID 規格的唯讀參考層，目標是協助 consuming firmware
repos 查找 HID descriptor、report descriptor、class request 與相關語義邊界。

## 目前狀態

- 已建立 HID class request governed matrix scaffold。
- 目前尚未建立 evidence packet。
- 目前尚未宣告任何 verified HID entry。
- 目前內容只作 reference scaffold 與 scope boundary。

## 參考入口

- [HID Scope](hid_scope.md)
- [HID Class Requests](hid_class_requests.md)
- [Verification Status](verification_status.md)
- [English Index](en/index.md)

## Non-claims

- 本 repo 不宣告 firmware behavior truth。
- 本 repo 不宣告 OS HID stack behavior。
- 本 repo 不覆蓋 consuming repo 中已確認的 project facts。
- 本 repo 目前不宣告任何 HID entry 已完成 verified promotion。
