"""SQLModel ORM models — Leapexbiz TCSP（公司秘书）业务域。

独立于会计做账(Part A)，仅含 TCSP 小程序 + 管理后台所需数据表。
"""
from datetime import datetime
from typing import Optional, List, Any
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON

# ═══════════════════════ Leapexbiz TCSP 业务域 ═══════════════════════
class TcspCustomer(SQLModel, table=True):
    __tablename__ = "tcsp_customer"
    id: str = Field(primary_key=True)
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    channel_code: Optional[str] = None
    source: str = "organic"            # channel / organic
    kyc_status: str = "none"           # none/submitted/reviewing/approved/edd/rejected/frozen
    tags: List[Any] = Field(default_factory=list, sa_column=Column(JSON))
    company_count: int = 0
    order_count: int = 0
    created_at: str = ""


class TcspKyc(SQLModel, table=True):
    __tablename__ = "tcsp_kyc"
    id: str = Field(primary_key=True)
    customer_id: str = Field(index=True)
    customer_name: str = ""
    id_doc_type: str = "hkid"
    is_pep: bool = False
    pep_relations: Optional[str] = None
    sanction_hit: bool = False
    status: str = "submitted"          # submitted/reviewing/approved/edd_required/rejected/frozen
    reject_reason: Optional[str] = None
    submitted_at: str = ""
    sla_hours: int = 48


class TcspNameCheck(SQLModel, table=True):
    __tablename__ = "tcsp_namecheck"
    id: str = Field(primary_key=True)
    customer_id: str = ""
    name_en: str = ""
    name_zh: str = ""
    precheck: str = "pending"
    icris: str = "pending"             # pending/done/blocked
    risk_level: Optional[str] = None   # G/Y/O/R/B
    recheck_count: int = 0
    free_quota: int = 3
    status: str = "pending"            # pending/done/locked


class TcspOrder(SQLModel, table=True):
    __tablename__ = "tcsp_order"
    id: str = Field(primary_key=True)  # ORD-...
    customer_id: str = ""
    customer_name: str = ""
    service: str = ""
    channel_code: Optional[str] = None
    amount: float = 0
    status: str = "待支付"             # 待支付/服务中/已完成/已取消
    created_at: str = ""


class TcspBill(SQLModel, table=True):
    __tablename__ = "tcsp_bill"
    id: str = Field(primary_key=True)  # LEA-...
    order_id: str = ""
    customer_name: str = ""
    service_item: str = ""
    amount: float = 0
    stamp_duty: float = 0
    proof_uploaded: bool = False
    status: str = "待支付"             # 待支付/待确认/已到账/已驳回/已作废
    reopen_count: int = 0


class TcspChannel(SQLModel, table=True):
    __tablename__ = "tcsp_channel"
    code: str = Field(primary_key=True)
    partner_name: str = ""
    orders_month: int = 0
    revenue_month: float = 0
    commission_month: float = 0
    settle_status: str = "待结算"


class TcspCommission(SQLModel, table=True):
    __tablename__ = "tcsp_commission"
    id: Optional[int] = Field(default=None, primary_key=True)
    channel_code: str = ""
    order_id: str = ""
    service: str = ""
    base_amount: float = 0
    rate: float = 0
    commission: float = 0
    period: str = ""
    settle_status: str = "待结算"


class TcspSupplier(SQLModel, table=True):
    __tablename__ = "tcsp_supplier"
    id: str = Field(primary_key=True)
    name: str = ""
    service_types: str = ""
    active_tasks: int = 0
    payable_month: float = 0
    status: str = "active"


class TcspSupplierBill(SQLModel, table=True):
    __tablename__ = "tcsp_supplier_bill"
    id: str = Field(primary_key=True)  # SUP-...
    supplier_name: str = ""
    service_desc: str = ""
    amount: float = 0
    period: str = ""
    settle_status: str = "待结算"


class TcspLead(SQLModel, table=True):
    __tablename__ = "tcsp_lead"
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str = ""
    source: str = ""                   # svc_detail/order_confirm/fab/partner
    intent_service: str = ""
    status: str = "待跟进"             # 待跟进/跟进中/已转化/关闭
    owner: Optional[str] = None
    created_at: str = ""
