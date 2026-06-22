# Leapexbiz

香港持牌 TCSP（Trust & Company Service Provider）公司秘书服务平台。从 `leapex` 仓库迁出的独立产品线，含**微信小程序客户端**与**管理后台**两端，共用一套 FastAPI 后端。

## 两端

| 端 | 路径 | 形态 | 用户 |
|---|---|---|---|
| 小程序客户端 | `/tcsp` | 微信小程序原型（HTML 模拟） | 终端企业客户 |
| 管理后台 | `/admin` | Web 控制台原型 | 运营 / 合规 / 财务 / 渠道 / 供应商 |

## 业务范围

KYC 尽职调查（AMLO）→ 核名查册（iCRIS）→ NNC1 公司注册（含章程）→ 回单支付 → 交付物（CI/BR/印章/SCR）→ 年审与变更。
含渠道差异化定价、渠道佣金台账、供应商应付、企微承接线索。

## 技术栈

- 后端：FastAPI + SQLModel + SQLite
- 前端：原生 HTML/CSS/JS（单文件原型，Tabler 线性图标）
- 图标上线注意：小程序无法加载远程 webfont，真机需改本地 SVG / iconfont base64

## 本地运行

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r ../requirements.txt
.venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8080 --app-dir ..
```

首次启动自动建表并写入种子数据（`backend/seed.py`）。

## 访问

| 路径 | 内容 |
|---|---|
| `/` 或 `/tcsp` | Leapexbiz 小程序原型 |
| `/admin` | 管理后台原型 |
| `/docs` | FastAPI Swagger（含 `/api/tcsp/*`） |
| `/api/health` | 健康检查 |

## 目录结构

```
backend/
├── main.py            FastAPI 应用（/tcsp /admin /api/tcsp）
├── db.py              SQLite 引擎（leapexbiz.db，运行时生成）
├── models.py          SQLModel：Tcsp* 业务表（客户/KYC/核名/订单/账单/渠道/佣金/供应商/线索）
├── seed.py            种子数据
├── routers/tcsp.py    /api/tcsp/* 接口（含 KYC 审核 / 回单确认 / 佣金结算 持久化动作）
└── static/
    ├── tcsp.html      小程序客户端原型
    └── admin.html     管理后台原型
docs/
├── PRD_TCSP小程序_MVP.md
├── PRD_TCSP_V2.3_客户反馈优化.md
├── PRD_TCSP_V2.4_服务模块电商化.md
├── PRD_Leapexbiz管理后台_v1.0.md
├── 技术开发文档_Leapexbiz管理后台_v1.0.md
├── 商业策划_海外公司服务_v1.0.md
└── 设计规范_Leapexbiz小程序_v1.0.md
```

## API（节选）

| 资源 | 接口 |
|---|---|
| Dashboard | `GET /api/tcsp/dashboard` |
| 客户 / KYC / 核名 | `GET /api/tcsp/customers` `…/kyc` `…/namechecks` |
| KYC 审核 | `POST /api/tcsp/kyc/{id}/{approve\|reject\|edd\|request-more}` |
| 订单 / 账单 | `GET /api/tcsp/orders` `…/bills` |
| 回单确认 | `POST /api/tcsp/bills/{id}/confirm\|reject` |
| 渠道 / 佣金 | `GET /api/tcsp/channels` `…/commissions`，`POST …/commissions/{id}/settle` |
| 供应商 / 应付 | `GET /api/tcsp/suppliers` `…/supplier-bills`，`POST …/supplier-bills/{id}/settle` |
| 线索 | `GET /api/tcsp/leads` |

> 管理后台 `admin.html` 启动时从 `/api/tcsp/*` 拉取真实数据；KYC 审核、回单确认、佣金结算等动作会持久化到数据库。

## 合规

香港持牌 TCSP，全流程符合《公司条例》(Cap.622) 与《打击洗钱条例》(AMLO)：PEP 含家属审查、UN/EU/HKMA 制裁名单筛查、EDD 增强尽调、资料 AES-256 加密保存 7 年、SCR 重要控制人登记册维护、不可篡改审计日志。

---

*从 `leapex` 仓库迁移 · 2026-06*
