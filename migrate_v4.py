# ASR Migration Script (Generated)
# Follows the same pattern as your migrate_v4 style using run(...)

def run(name, query):
    # Placeholder: your actual run() implementation should execute the query
    print(f"Running: {name}")

# ── ASR OFFICERS INSERT ───────────────────────────────────────

run("Add ASR SP",
    """INSERT INTO officers (id,name,rank,level,report_to,password_hash,created_at)
       VALUES ('ASR_SP','SP ASR','SP',0,NULL,'file_managed',now())
       ON CONFLICT (id) DO NOTHING""")

run("Add CC to SP",
    """INSERT INTO officers (id,name,rank,level,report_to,password_hash,created_at)
       VALUES ('ASR_CC_SP','CC to SP','CC',1,'ASR_SP','file_managed',now())
       ON CONFLICT (id) DO NOTHING""")

run("Add Addl SP",
    """INSERT INTO officers (id,name,rank,level,report_to,password_hash,created_at)
       VALUES ('ASR_ADDL_SP','Addl. SP ASR','Addl. SP',1,'ASR_SP','file_managed',now())
       ON CONFLICT (id) DO NOTHING""")

# ── DSPs ──────────────────────────────────────────────────────

run("Add DSP Chintapalli",
    """INSERT INTO officers VALUES
       ('ASR_DSP_CHINT','DSP Chintapalli','DSP',2,'ASR_SP','file_managed',now())
       ON CONFLICT (id) DO NOTHING""")

run("Add DSP Paderu",
    """INSERT INTO officers VALUES
       ('ASR_DSP_PDR','DSP Paderu','DSP',2,'ASR_SP','file_managed',now())
       ON CONFLICT (id) DO NOTHING""")

# ── DCRB ──────────────────────────────────────────────────────

run("Add CI DCRB",
    """INSERT INTO officers VALUES
       ('ASR_CI_DCRB','CI DCRB','CI',2,'ASR_ADDL_SP','file_managed',now())
       ON CONFLICT (id) DO NOTHING""")

run("Add SI DCRB",
    """INSERT INTO officers VALUES
       ('ASR_SI_DCRB','SI-DCRB','SI',3,'ASR_CI_DCRB','file_managed',now())
       ON CONFLICT (id) DO NOTHING""")

run("Add DCRB Seats",
    """INSERT INTO officers VALUES
       ('ASR_DCRB_D1','D-I Seat','Seat',3,'ASR_CI_DCRB','file_managed',now()),
       ('ASR_DCRB_D2','D-II Seat','Seat',3,'ASR_CI_DCRB','file_managed',now()),
       ('ASR_DCRB_D3','D-III Seat','Seat',3,'ASR_CI_DCRB','file_managed',now()),
       ('ASR_DCRB_D4','D-IV Seat','Seat',3,'ASR_CI_DCRB','file_managed',now()),
       ('ASR_DCRB_D5','D-V Seat','Seat',3,'ASR_CI_DCRB','file_managed',now()),
       ('ASR_DCRB_D6','D-VI Seat','Seat',3,'ASR_CI_DCRB','file_managed',now()),
       ('ASR_DCRB_D7','D-VII Seat','Seat',3,'ASR_CI_DCRB','file_managed',now()),
       ('ASR_DCRB_D8','D-VIII Seat','Seat',3,'ASR_CI_DCRB','file_managed',now()),
       ('ASR_DCRB_D9','D-IX Seat','Seat',3,'ASR_CI_DCRB','file_managed',now()),
       ('ASR_DCRB_D10','D-X Seat','Seat',3,'ASR_CI_DCRB','file_managed',now()),
       ('ASR_DCRB_D11','D-XI Seat','Seat',3,'ASR_CI_DCRB','file_managed',now()),
       ('ASR_DCRB_D12','D-XII Seat','Seat',3,'ASR_CI_DCRB','file_managed',now())
       ON CONFLICT (id) DO NOTHING""")

# ── AAO ───────────────────────────────────────────────────────

run("Add AAO DPO",
    """INSERT INTO officers VALUES
       ('ASR_AAO_DPO','AAO DPO','AAO',2,'ASR_ADDL_SP','file_managed',now())
       ON CONFLICT (id) DO NOTHING""")

run("Add AAO Seats",
    """INSERT INTO officers VALUES
       ('ASR_AAO_A1','A1 Seat','Seat',3,'ASR_AAO_DPO','file_managed',now()),
       ('ASR_AAO_A2','A2 Seat','Seat',3,'ASR_AAO_DPO','file_managed',now()),
       ('ASR_AAO_A3','A3 Seat','Seat',3,'ASR_AAO_DPO','file_managed',now()),
       ('ASR_AAO_A4','A4 Seat','Seat',3,'ASR_AAO_DPO','file_managed',now()),
       ('ASR_AAO_A5','A5 Seat','Seat',3,'ASR_AAO_DPO','file_managed',now()),
       ('ASR_AAO_A6','A6 Seat','Seat',3,'ASR_AAO_DPO','file_managed',now())
       ON CONFLICT (id) DO NOTHING""")

# ── TECHNICAL ────────────────────────────────────────────────

run("Add Technical Units",
    """INSERT INTO officers VALUES
       ('ASR_OW_CYB','Inspector Cyber Cell','Inspector',2,'ASR_ADDL_SP','file_managed',now()),
       ('ASR_OW_COMM','Inspector Communication','Inspector',2,'ASR_ADDL_SP','file_managed',now()),
       ('ASR_OW_IT','Inspector IT Core','Inspector',2,'ASR_ADDL_SP','file_managed',now()),
       ('ASR_OW_NDPS','Inspector NDPS Cell','Inspector',2,'ASR_ADDL_SP','file_managed',now())
       ON CONFLICT (id) DO NOTHING""")

# ── DAR ──────────────────────────────────────────────────────

run("Add Addl SP DAR",
    """INSERT INTO officers VALUES
       ('ASR_ADDL_SP_DAR','Addl. SP DAR','Addl. SP',2,'ASR_ADDL_SP','file_managed',now())
       ON CONFLICT (id) DO NOTHING""")

run("Add DAR RIs",
    """INSERT INTO officers VALUES
       ('ASR_RI_ADM','RI Admin','RI',3,'ASR_ADDL_SP_DAR','file_managed',now()),
       ('ASR_RI_WEL','RI Welfare','RI',3,'ASR_ADDL_SP_DAR','file_managed',now()),
       ('ASR_RI_HG','RI Home Guards','RI',3,'ASR_ADDL_SP_DAR','file_managed',now()),
       ('ASR_RI_OPS','RI Operations','RI',3,'ASR_ADDL_SP_DAR','file_managed',now()),
       ('ASR_RI_AR','RI AR','RI',3,'ASR_ADDL_SP_DAR','file_managed',now())
       ON CONFLICT (id) DO NOTHING""")

# ── FIELD (CI → SI) ──────────────────────────────────────────

run("Add CIs",
    """INSERT INTO officers VALUES
       ('ASR_CI_KOYYURU','CI Koyyuru','CI',3,'ASR_DSP_CHINT','file_managed',now()),
       ('ASR_CI_CHINT','CI Chintapalli','CI',3,'ASR_DSP_CHINT','file_managed',now()),
       ('ASR_CI_GKV','CI G.K.Veedhi','CI',3,'ASR_DSP_CHINT','file_managed',now()),
       ('ASR_CI_GMD','CI G.Madugula','CI',3,'ASR_DSP_PDR','file_managed',now()),
       ('ASR_CI_ARAKU','CI Araku','CI',3,'ASR_DSP_PDR','file_managed',now()),
       ('ASR_CI_PDR','CI Paderu','CI',3,'ASR_DSP_PDR','file_managed',now())
       ON CONFLICT (id) DO NOTHING""")

run("Add SIs",
    """INSERT INTO officers VALUES
       ('ASR_SI_MAMPA','SI Mampa','SI',4,'ASR_CI_KOYYURU','file_managed',now()),
       ('ASR_SI_KOYYURU','SI Koyyuru','SI',4,'ASR_CI_KOYYURU','file_managed',now()),
       ('ASR_SI_CHINT','SI Chintapalli','SI',4,'ASR_CI_CHINT','file_managed',now()),
       ('ASR_SI_ANNAVARAM','SI Annavaram','SI',4,'ASR_CI_CHINT','file_managed',now()),
       ('ASR_SI_GKV','SI G.K.Veedhi','SI',4,'ASR_CI_GKV','file_managed',now()),
       ('ASR_SI_SILERU','SI Sileru','SI',4,'ASR_CI_GKV','file_managed',now()),
       ('ASR_SI_PEDABAYALU','SI Pedabayalu','SI',4,'ASR_CI_GMD','file_managed',now()),
       ('ASR_SI_GMD','SI G.Madugula','SI',4,'ASR_CI_GMD','file_managed',now()),
       ('ASR_SI_MUNCH','SI Munchingiput','SI',4,'ASR_CI_GMD','file_managed',now()),
       ('ASR_SI_ARAKU','SI Araku','SI',4,'ASR_CI_ARAKU','file_managed',now()),
       ('ASR_SI_ANANT','SI Anantagiri','SI',4,'ASR_CI_ARAKU','file_managed',now()),
       ('ASR_SI_DUMBRI','SI Dumbriguda','SI',4,'ASR_CI_ARAKU','file_managed',now()),
       ('ASR_SI_PDR','SI Paderu','SI',4,'ASR_CI_PDR','file_managed',now()),
       ('ASR_SI_HKPT','SI Hukumpeta','SI',4,'ASR_CI_PDR','file_managed',now())
       ON CONFLICT (id) DO NOTHING""")
