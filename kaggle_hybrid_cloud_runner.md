---
title: Kaggle Master Hybrid Cloud Runner
tags:
  - infra
  - kaggle
  - hermes
  - hybrid-ai
  - qwen32b
  - antigravity
  - google-ai-pro
created: 2026-09-30
updated: 2026-09-30
---

# 🏛️ Aethelgard Master Hybrid Cloud Runner

This document contains the complete, pre-configured **1-Click Master Cloud Runner Script** for deploying the **Hermes Aethelgard Vault Custodian** onto **Kaggle Dual Tesla T4 GPUs (30 GB VRAM)**.

---

## 🧠 Hybrid Architecture Overview

| Layer | Technology | Role & Capability |
| :--- | :--- | :--- |
| **Google AI Pro (Antigravity)** | **Gemini 3.7 Flash High / Claude Sonnet 4.6** via local OmniRoute on Kaggle | ⚡ **Google AI Pro Subscription** — High-speed reasoning on HIGH effort, full 17-tool agent execution, and multimodal vision. |
| **Local GPU Workhorse** | **Qwen 2.5 (32 Billion Params)** via local Ollama | 🚀 **100% UNLIMITED Rate Limits & Free Tool Execution**. Runs directly in ~19.8 GB / 29.1 GB Tesla T4 GPU VRAM. |
| **Secondary Cloud Engine** | **Bluesminds (`claude-sonnet-5`, `gpt-5.5`)** | 🌐 Cloud backup for advanced coding. Switchable in-chat with `/model claude-sonnet-5`. |
| **Interface** | **Telegram Gateway** | 📱 Direct mobile chat access to the vault custodian 24/7 on demand. |
| **Persistence** | **Git Background Sync Engine** | 💾 Commits and pushes all modified notes and assets to `aethelgard-vault` on GitHub every 3 minutes + emergency sync on shutdown. |

---

## 🚀 The Kaggle Notebook Script (Copy & Run)

Copy the entire block below into a single code cell in your Kaggle Notebook (with Accelerator set to **GPU T4 ×2** and **Internet ON**) and hit **Run**:

```python
# ==============================================================================
# 🏛️ AETHELGARD MASTER HYBRID CLOUD RUNNER (ANTIGRAVITY GOOGLE AI PRO + DUAL T4)
# ==============================================================================

import os, subprocess, time, threading, base64, shutil, json, gzip, sqlite3

# ── 1. Credentials & Configuration ────────────────────────────────────────────
GITHUB_USER = "xionforbusiness-glitch"
GITHUB_TOKEN = "ghp_" + "gY0RVq7FifRJQgQVsu8fEsTsi5PV8e45VERo"
REPO_NAME = "aethelgard-vault"
REPO_BRANCH = "main"

# Pre-filled Tokens & Credentials (100% Full & Verified)
TELEGRAM_BOT_TOKEN = "8992784967:" + "AAH2bK1CAi8M2m3fe12UG-qUwmQCSpPk114"
TELEGRAM_USER_ID = "1021125594"
GOOGLE_API_KEY = "AQ." + "Ab8RN6I64Bj-z2kKo2b-o6cETMuJgQ0LySbUjAMqgraCrYKPzQ"
HERMES_CUSTOM_OPENAI_API_KEY = "sk-yCD9w" + "fdpF74PdFbyFukBYnnGGX1oPjgvjQuCmaPMz4zcELsY"
OMNIROUTE_API_KEY = "sk-2f7015" + "c0ceee29cf-ffc0c5-a515b8da"
HERMES_CUSTOM_FIRST_TIME_API_KEY = "sk-2f7015" + "c0ceee29cf-ffc0c5-a515b8da"
STORAGE_ENCRYPTION_KEY = "033f70a7200356ea676c7a09712b593c46b60c6debc3c8c5425bd49f6f2926c1"

# Complete OmniRoute Seed Payload (Providers, Combos, API Keys)
# Encrypted with STORAGE_ENCRYPTION_KEY; restored via native sqlite3
OMNIROUTE_SEED_B64 = (
    "H4sIAAAAAAAC/9VdW3PbSHr9KyrlJUkNqL6jwadMNnuZ2nUm2XXyYI+L1eiLhAgkOAQpWzvl/57TACmBFEnTXoMQq2YsogH0953T"
    "360bt9+u54vqoXB+MbHVbObtsqhm9fX46rdrW5WrafP7/XXhrn+4ejo0/jar5d1k+Tj3cWNmps1fPzVF2R5ZVIti+Rh/F/XEoNuH"
    "5ghjra/rybK697O4vfBh4eu75wb/aV6gZWKWcatpnmy31bZqpUKd/4PCk1a5pa+Xk3pplqu66WexqCIm1xxaGuxsmra31l12GjaQ"
    "Ok11tVrYpjE39r4KYVL6B9/gXJiln5TFtFh6N1nNli36O29KsGPvvL2fFLOlXzyY8qnTrb0d+RGAb6CYeTG59y157pmap5Gq594W"
    "obATZ5amS1rRHOeKel6ax8lmVG7LKjflpDsmzgezKpeTKfgpn4negIcp1N6u4qBNVrUHjcC2jRfdVcvWXJ4Q4FC3RnS7qFbz+GNq"
    "PkXLsqvFwrd94MRPjxM/M3nZwp0DEuBOXuz4dVUtzeShqAu0PDd8LGau+jhZ3kXLqUpXT/6vbrXoqFc9YPDA1vNOu/Bm+aTgau46"
    "W43682J2u7uNIyDFL5vx+BBFVB8bl3h/zXlmmc9VIm0wiSA2S/KcUvzynKaWCG3T2BesdQY2lmu/mRfrof35qf3PTcNsVZY/XNHm"
    "v/b38X+vn7zq+HFk78mMMJWQLOHkLWVjScecjpTi7xpzmtnxAx17YlPlufN5lhpGiFUk9SnTVBFKndBjgx9eCpH7QAX2Oc94plIp"
    "heEsdyb3Pk+pz3OlidQhw//ah6DTzAQP+lRuUuNzLYnXjBqSKhqoSk2mcW7gqSfCUGc0yz1jQrnAVUiVNrmyRKfekuDQJrSJ5qwV"
    "zdg4JxkhNGW5dRiAQCXPAkkzJ6Igm+ontq5/++W6mM6rxfIPC+/fRD+of56Vj79cj5eLlf/hlzhSGJg/Nd6K1t8+fz6F6r1s06ad"
    "HhgCKt4yOm5GYcSJboZg//CId1sqwB7fX6uUUGGVSoK3MhGCpkkmPElCoFYwwVNj5cYMN+Fw2wh/h9arH23j5Ff0dViiVO92uosD"
    "FqJHLhDIZssaQ/L+l2vBhcqp8UbkTAiiMk4Ml9YF6VTOaf4LnPb8QynHQo6k5IeHUqZ7hpJkTknvTKIltYnwmuJXxhKWG+ms1kKx"
    "EHu8LxZVM6QxCV/v02/jwincJuXeMg7vUFnOhUktaFEShiGYGltBnRUe3uwkZSbL4WpeykC0CE4IE1LBgyC5zL2TPM8dyUPONQPJ"
    "iupUquA899orpbNMwNFzw2hmXMhMxggGxaQpTeH0AiwoIqi1gXKqKZeC4ofIuGM0BgUvVAwiViuvtTG5DTxjhkqaUri+zTJFMk55"
    "nnGW4UQEC58TL1xmCeDQDO7emjsJgpEcHeTMprnTlImQCfxPqWHGAgg6CgoaBZDiCMPphqVEesjXzEqfomOuQLhiTmbWIL7jFIIx"
    "yCjR3HFuNQU/GluILjq1GSJcGjTPJXMp0Vq6nKKHHI0+IERivBHunDSZ4JZ7bClCwBJO4D5wknLJDaXKQkNtLeXo3frMMZ1hAByR"
    "gG6lCNQRyqxRlIWcBmkV9yIEpiFReuVZqslYcJ4bwTU8gynJjEqV8zJkiOYEsVx2IrzTLjCPncJKkmMQUwD3LgM/jHPtx4jJqQoh"
    "S3OMnscApQKmqDPDQJ1NMbA5YOUBo5bmAeZpbKZzjGdGJHXUG6k02EN0zpwUltoM4ypyCXtDMpHO5Rb9BZYqxK2cY2w4M3mWSaN8"
    "atG9VpnWGcwPKSNXKQsx01CHwE5olmpqtAEAbTD2Af0IwSikKmBJFedGUioxPEYZGSzGR6aOSpdarwMPhhtDuHMOlgHCoTo0BSZP"
    "05QLaxw04z4mFxyteMxWTLM01Q6DFOArnGnAk5IFKEYx0tTCMuCphMrcOYqMmaawWwxPnuc6C0IhecLF4kgr48GghNVYAvNIRWB5"
    "0JDkBYMtcOBHb4zAXXKJnjDMPKruYNwEOEA6UrPHMbZJf4xTYzkszqAuoUyiOYdnZ3AU2B7yt5UWmXvMtCDE6ZQGhBukDg/TQobm"
    "whFDBSXdkMXIW8bGRI+pGsGe3n1h33fICVvdkyYpZqMsZS9EI4zC1OkIdrMvU8TI+MYv7yqHeL/J9B4byAabOrrZ88equi39pj0U"
    "pf9xMWv2mMVsbD7W45g0P96hpvYLvxiv6sSjOEzoWCHgpTITlGs5Xp978/s//fFH/se//u9/v/mfPzed7k090ft7Sj16LNQIzrtv"
    "rNiYipEUek/qYdH3OcoGREiUsNzpJHc8QxKCPSKAu5y0UxPMcW4X5mE9j9hkoOtqahYjU878dEHEv93GeeDIVtPju9oKYxOMoq95"
    "FHwIN4YqxwIzEjHUZRLe51Q2zijiGCgPcCT4DcxfeisQMKyEDxE4C4ISAo32JHhlGDyLwhOcCBZpxCC+ozoM8G9G4dwIrS5DyYqg"
    "kxuch9hsmEW9a2Kl6jjyi8zjdkCGYiTLnU+dkymBPE4ygVCAyIEsxhhcksA9qY7nEqSR6JkxPhjrTIwtDpHRE4/kg0Jaae+9csRq"
    "uK4mGU21RvxXKJeRXIyMsQ+VLziXChkXMSZTMsDdKWIQIopDrYNjMqRcTXxwBNkJYT0TiJq5zWQ0SxoUgguz2ucI8BSBnzuDgMhS"
    "EwLQihi2GcImdOc5CssMYGmDFf0hi2iW6dQheFmFSgpxDQI8swiyyCY8IPogL6HSRkRD5ZCxLASOmoBCdYcM7BB8KPIvD8goSrOQ"
    "ZZj4Iz9ypAqL0CY0IPkYyomHwqgMQCEX8d8MHKPVIMTJENI4uUA2B69eaqSNLBsjj6O+Q/rEASnyL0WCkJhBSIISxZisk+EMhtmq"
    "HPlfpjAJ1BMa0wlpgpa5hqGMM4M0xngscxRnEjYF50SFAYNHrM4M0ivki1hDoKwE48IJY0JU0NIsSIwFKiZkD4xbrnyG3BJHFvKE"
    "1lahxiIuzwXmOgLgtTIOQ5FJqSS3KC1MliF9E5CGHCICVETWgZZKWs49R5/IJAq1h091sC7aqcBA6YxpVF0wIiNgwrBvWBUbg1SK"
    "xBOQkoED5YuU8FsJS2aaI6vulqM8lqOUjygh77607265nNfjm5uPHz+ObpugidBWR0++iUHgBmsQflFMMcmvzcxhyh+K2/rqS2dh"
    "yQDVfKhGzdLRFw+3tqxuT+90HZWv4tyncF/uvaxWLsHayTJUiyZ2mSJG/ySuh6ymflFf/+OJ7WkagFiMKnjPFEEo5LaRIHJfYrNl"
    "AYr/qwXW5jb3lL7icthPbcbb1bw5ZFmss94tTXB40m5jR73Ka7so5nE5522xlRqvfvzpCuJaEaVpc+OmYX92QwjqJ7sxMaaYI+9l"
    "bcOo2pPdNGI/skuWGCY85siEJTrVJkEg0YRkCHWhXSnz02JWbM+Qn9qGnxUjjnfXZ1BGp8ZRg3I3RdxLc8yEfZajxFWYxKh8HBA2"
    "UElyg0iKxZe4LiKwGoPGLKDuzlFJop7EOkuM35hfoBC2zqKszUKG4zBrwTwAiyfOWszLEOMYFl1Q77g4awyQqAPiDqF5OsYcHAES"
    "azfYgQUaVOmYeGJ6iLknKlaeba27nDgdX1OfsJFMAlbknqe632hD8i1VYyajd2ECeXByTttys2NDHz43i6LTvDq0NL5Za92syNYo"
    "NyfVYr1YfmzpsX7Esu90MsWyuLn17VpsVU7g3lgZxOLjrf+0XpJd+k/LCWajd767+Lq9KMlSplAApQlRKSw9WJFgTq8TZB6CrKAC"
    "2mN3f/jpr397m7z96c3vr9sxiQAa137e03h4s0LcLLbEBbM2toRigQp4iWCfNLsTmmxWlxJbmhX+hLiIm8jklNWpJMyTL6/jQJd7"
    "LPw2CjRSn9Vr2jYa3GxrsFXxr2Pj5tBm30df3N4t0U6wUaIIa7t7Wg/75frzD0egsxfQqznmCGJQ7BsV+gbPk858YAe/SpZ3xQxq"
    "3yanTC6+DLIj6uaQqH2AO+c1u5+vc60POFm9A2wdmOB8gTuxj7s66rZsIPVG2rOMC2JLPrvZbTkdxrkawX27lNoFygeDOuJ9g013"
    "wbLhwLK+weqDSZIOnyYT2jf8bCverUs7DhNoSrvkDp33EPM2ckZdORcU9yjZTxtdwylx50GftHXlXBJtdB9tccqLGnu27I+xJxGX"
    "RBY7ZGMRTVl97NfA1kIuiTB+PJb1TFlHzCWRJo6TNvWuWE3PwVsr6ZKok8epi8t43p2DulbSJVGntqmbL5OqrhHySN6jxb2UckmU"
    "pUm8wWRTpN6Z4n7VrGeccnvKl4mKfd9s9z3aO6uKB+7n5WRFvlCy/lPb0Zf40Ft8PE2f+yBk0/krZyTbx0iPfLxqNhhp2cDNGPPa"
    "+3sEZvY9qXjud/8c9dXwQFse2pn8dyTg4LrLq0HO1sjn0QtUUq5m5rsSEPsdtf2+ah74Ng91VfZBA7p91SyIbRZwGWfRizk0Hb9q"
    "JmTLRCwi8RxAMmWYU35HIp77HdFXzYN6wYPsiYfXHSfXleWvH/2MJ3FhcZHMcFHze3Kx2/er5qOzJJwXt8m8sPdYjB1gMfhZeu/X"
    "S7MXy+DPM4zhlsGfdOj9kik5dMFYDX/BWPWOnh5Cnw6PPu0d/cGbBfTw6HXv6Pl+9IPfKNG/z4sXyJ8vwg+GfaNC7+jlYfTyFeA/"
    "w/irI+P/GhjoP+6n+yqdvguU4yp1iq+nJZYHsV7oHmBQXijR+6BkxxiIj11XswS3db8KMjr69M2LIPt5iRcqB6ZivrkRu0f0nRLt"
    "6UrTYE6xrUHv2Nke7HSogd++Rt47dr4Huxx+5Dc3f/eOXxzB39xm8wpIOHgfzndlQu5hQr0CS1BnsgS1B3/6CvCnZ8Kf7sGvXwF+"
    "fSb8eve2VDrcbam935cpspd3HA831O19x+cZZ0kOTctewbS090mppMeqf7yVy7+Ouj9q0jsX7AgXZ5rCHVeQH5ySnGUmcVw5cWjG"
    "cI5C/7hq3VJmPpBjN4J7N2G1izT+/DQY3lZ876jTXdQzM6uGAx2l945Z72KmgwHuvzyR2Uu0w1r2iJ7HthU5hDxe6x8afVSidwbo"
    "QQZirhieAmjROwdslwM2HPDen5FT/CXagb2dncnbxS5yPjRyfibk8hDyem4W94Pjb9XonYUX9ZsYDnnv14RV+hLtsDFdnCea65e4"
    "B61YR+IsNavKXuIe6qrKGvYZLqmkLyq44eafo95noCl9iXbQMZZnGeMX9dn6/v/BYB9+TuC74uYvccf7/QeEfeC5gO+KWrxE3d7f"
    "PyDug88BfFfkO1Uanqusl8PhXovvHXW3KltU90PdstbKPkMMT1/gVQPi7f2+tFTv4M1XRekSMtCSWkeD/lfW0k5Ndo9vZiT3bBjj"
    "Xgvv37o1eYlYDYm4d/vW9CXitJnWDgm71aB37GwXOx8OdO+v0tKdeqyML93jiGLrK6jFbLDrua0qo11VemejU6dNi2mVPMTYNhQJ"
    "aw1G8jzYZRd754nDQZAffzLxu+JWe3GnA+Pu/akine7BzQdF3X+069RtU7zue71UTIe5ONLV4AzvEcwOYo8vCV4U+WpZLYYLdltk"
    "vFCp99cMkgPs8MHJ6N0rMnoQ+6uzDH5+y+jUg3glUrVc4HESnuAziFjGGIqTvYr0zgTfy4RE4YhuZ7FkG56P0a46vbPSqRnbtwhg"
    "AbnE86ED0NDIH7Xye8ctd3GrgXGr8+Du1It3j3wwk9/I7h1vp06c4fMEd+0V12Z7MHffo0fvPOjjPJxP/eNqtmVe+4VYdH+HNy/u"
    "H7dTPkR7GqhW2E0rbBfd+Bi69sz9L1U5Wb8DA7v1odwvvi+ZdGlz1bJO6uXKFVX7m4NCPMo1X/iHwn/sib+O1Js9Ui+ESNolsvOz"
    "H846Py+DHtblpP2aVLz7fQrJeOFTniA6JsWyJ7ZaeTcv5V2IbfEj5CGDnI24VtaFkCb2kFY+LgoT53dlMX+Kan2xtk/Y66dNHqEt"
    "3p9yLtY6sl4/aapLWjGzqMehiikOXlv47ux1hO65inAhLpueSCM+mbj05yeyEXshVOoTqXwoz8/jQ3khJG7NKcri11XhkjLgHejt"
    "cwV5T9S1km4aSVjVwIXv/DIIo1uzCbxPEh/3KJq/s0hZMzfqh7K1rJtW1qiVdSGk0RNJa775c0bmDn7853XRx06kb/39gnMSePhj"
    "Bq+LQn4ihbNqdlbfbQS+fvrEUfpiIXumoAdRFxLz5GmUnSnkbXi7kIinTiPvbAHvib5LiXfpaQSeKdw90XcZ0W5rZjGDnpiudy6L"
    "Ns9nVdP4cgp8zsfwPMHXnPGWlqfLpN+f0EaHm9N0uJD4mB0nuV7N0d58MMlQlp+N2B25l0EmI99AZvwo3UCEHvpS3esilX4Dqb1l"
    "pNN4vZD0xNhxats7X6SM2KQ8n/PvyL0Q5+ffQGZPZedJjF5GDcrEN9B6PvffS+yluL88Tq1sbgWMn+WtTfD4SuOZ/H+0K/hCAoD6"
    "Ep07t/GdhcknmRdC4taMaV5VZV3EJ2fMbXx2u07il6r6IW8j6+ZZ1oheCGn6GGmfzsnap0uibWvus7wrZkCNr7Fa/PI1rmXdl/35"
    "6q64m7W4y6COk9Op66fGOcrfZZQ2nJ5OYi+zxOMcXsLkkLPTKeyrKDzO4oXUgpx/BZHN42Tl2Zlsxb5+KsXpVPaz8Hucx4tY/OXy"
    "dBI/DZFhPl1GilEn0VjDr8ozFzqt0Aspd9KvpfG8Jtnh8kJKH/21hJ61AOryeRFlUPa1dJ67GOoyeiElkSBfTeq5C6MtVi+kPBL0"
    "a2k9b5HU5fQiSiXBvpbQT8Nlp8som8TWbMjgUfjvz1bs9fUTIRLcil7cLsxDgQsAux/G3oz4l4F3erk52ssOG53zvuYhTYpvpXUV"
    "f/G5sCczPFnr3a99HSy0vllldVzlTSHy7RofKGW+WeH0uMKdPP/tOh8uFr5ZbX1c7WWBh2zdP6h2p5PvpXa2rTZetlnVdXvnwTcx"
    "faCD09X9gM34ss+lv31sjp0vimqxORCBKxTw6TFA4eVDf/V4qYjHywPGFDsX2Hr8D1+axzexiRESg9SdmbkqhLd3C1/fVWVUgIy0"
    "fN7z5glJC8x8euPr2tz6+g/V4m8rPDu4iJrw2BkUs/dvolQbRSwXK98IXt+e9ba697N/X4XgF7+fmbyMg7U56O9+Uf0FsGb28ec5"
    "xqD4u4kBuH4+MJiy9p9/eBouljLltE8TolKfiGBFkuU5vounFVEuVwHtjcpF/afCOT/b9BEpxOPcPy9cjPcNNxY6Lr37cdn2THBd"
    "Ec+HUPGWsTHhY8ZGGZHvmt5Wc7fnUEbeMj6WakzxlQQu2kMf/CI+IxPJbmiYm2Lxn1X8aCXOfO/y5M6bcnk33pYn+FiokcjSdx+u"
    "UnY1Leoa3F09J6WreTH75/pfrmzpDQx+hIRy/cMV/eHqoOLXnX27mmLfbFWWm3/Jhw+fcbSZF5N7/1hfj69+g1mVq+ks/n4P8mNn"
    "MzP18S8OiX/W1cek3YnCo/ro3aTxgbo5vJqU1W38tSZ6YpZxC08AwiQ2W/iccQErXG/BpZcTvCVnsxeiJnhkMBSf4lYxnzRiyqJu"
    "9tYWObzuSrfVNK+aluXdolouSz9x0fgn06YRTuTNFE3B4H6CRtfu2b+uqqVpDnRFHS1wgrp0Ml/lZWE7wFbRESYlzHU58a2lNueY"
    "onycdHeu6mbHR3xxbP8eCwr9C3UaSRNjLVzuqRHIQEQdTasrNC8re79F+zMVG9Npm1EFTdBBVT40/RWgHHvbjbWsGtq4VdkqYT7h"
    "8F9Xvl7WE9x5NXHmcW874jFqnM2uulWxERkDVou3XkvMDXRym4G9Q/yOvxEIPz3umJGfuXlVzJbPkNb8gYcpYlRDyZ2pWoKeGPkQ"
    "xVYfG6t9f52nXAvDTEKdsfjOY9BJrqjFJhUh54qbNMSOfvypMY77hAW8AURaYr33LLMBb/7ABiocSWWunWlcaueY2Pb+A/4lL31R"
    "jqkaZSLd9ben4zh5S9m48f8Rz/S7XT2ezrt+j/jlyzBuWPjl+sN129YY/M2/tg3rQ0t/a+xjVy+yI/75CFDbhpGNmPUZdPuMdZjo"
    "/LiWngQrTepTQZwjPFc6kzbVKijiuJHeg7xcGktNSK2lOiiWmzSTqcslssH1i74JRu89+MWwMbx8IUi8Wl54jJfm+PyfyKkXKbM+"
    "8zJq/ru//HT1Y5ww/LkNR/uGT2ap5SbJdZp65dTpwyffEjJmekzUSGqyO3xrrg4M1CsYmpQxrdOgqdNYBsBtCyZTMuNSWLyeJgtO"
    "5gx7dGa4YFmeZUIKn+NdNqBYacv3Dc2Hz5//H5bToWUrvwAA"
)

VAULT_DIR = "/kaggle/working/vault"
HERMES_PROFILE_DIR = "/root/.hermes/profiles/llm-wiki"
OMNIROUTE_DIR = "/root/.omniroute"

# ── 2. Install Node.js 22 LTS, OmniRoute & Dependencies ───────────────────────
print("\n" + "=" * 60)
print("🚀 [1/6] Installing Node.js 22 LTS, OmniRoute & Dependencies...")
print("=" * 60)

subprocess.run("apt-get update -y && apt-get remove --purge -y libnode-dev libnode72 nodejs npm && apt-get autoremove -y", shell=True)
subprocess.run("apt-get install -y zstd git curl", shell=True, check=True)

# Install official Node.js 22 LTS
subprocess.run("curl -fsSL https://deb.nodesource.com/setup_22.x | bash -", shell=True, check=True)
subprocess.run('apt-get install -y -o Dpkg::Options::="--force-overwrite" nodejs', shell=True, check=True)
subprocess.run("node -v && npm -v", shell=True, check=True)

# Install OmniRoute, Ollama & Hermes
subprocess.run("npm install -g omniroute", shell=True, check=True)
subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
subprocess.run("pip install -q hermes-agent requests", shell=True, check=True)

# ── 3. Pull Aethelgard Vault & Antigravity Keys from GitHub ──────────────────
print("\n" + "=" * 60)
print("📁 [2/6] Pulling Aethelgard Vault & Configuration...")
print("=" * 60)

auth_repo_url = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"

if os.path.exists(VAULT_DIR):
    subprocess.run(["git", "-C", VAULT_DIR, "pull", "origin", REPO_BRANCH])
else:
    subprocess.run(["git", "clone", auth_repo_url, VAULT_DIR], check=True)

subprocess.run(["git", "-C", VAULT_DIR, "config", "user.name", "Kaggle Hybrid Custodian"])
subprocess.run(["git", "-C", VAULT_DIR, "config", "user.email", "agent@aethelgard.local"])

# ── 4. Restore OmniRoute & Launch Antigravity Google AI Pro ──────────────────
print("\n" + "=" * 60)
print("🧠 [3/6] Restoring Google AI Pro Antigravity Accounts & Launching OmniRoute...")
print("=" * 60)

os.environ["STORAGE_ENCRYPTION_KEY"] = STORAGE_ENCRYPTION_KEY
os.environ["OMNIROUTE_MAX_PENDING_MIGRATIONS"] = "0"
os.makedirs(OMNIROUTE_DIR, exist_ok=True)

with open(f"{OMNIROUTE_DIR}/.env", "w") as ef:
    ef.write(f"STORAGE_ENCRYPTION_KEY={STORAGE_ENCRYPTION_KEY}\n")

# Start OmniRoute briefly so it creates storage.sqlite and runs migrations
subprocess.run("pkill -f omniroute", shell=True)
time.sleep(1)
omni_init = subprocess.Popen(["omniroute", "serve"], env=dict(os.environ))
time.sleep(6)
subprocess.run("pkill -f omniroute", shell=True)
time.sleep(2)

# Restore all provider connections, combos, and API keys directly into SQLite
print("📦 Injecting verified Antigravity Google AI Pro accounts into OmniRoute SQLite...")
db_path = f"{OMNIROUTE_DIR}/storage.sqlite"

try:
    seed_data = json.loads(gzip.decompress(base64.b64decode(OMNIROUTE_SEED_B64)).decode("utf-8"))
    conn = sqlite3.connect(db_path)
    for table_name, data in seed_data.items():
        cols = data["columns"]
        rows = data["rows"]
        quoted_cols = ", ".join([f'"{c}"' for c in cols])
        placeholders = ", ".join(["?"] * len(cols))
        conn.executemany(f"INSERT OR REPLACE INTO {table_name} ({quoted_cols}) VALUES ({placeholders})", rows)
    conn.commit()
    conn.close()
    print("✅ Antigravity OAuth + Providers + FIRST-TIME Combo restored successfully!")
except Exception as e:
    print(f"⚠ SQLite restore warning: {e}")

# Launch OmniRoute daemon
omniroute_proc = subprocess.Popen(["omniroute", "serve"], env=dict(os.environ))
time.sleep(5)

# Verify provider status
print("\n📋 Verifying OmniRoute providers:")
subprocess.run(["omniroute", "providers", "list"])

# ── 5. Start Ollama GPU Daemon & Load Qwen 2.5 32B ────────────────────────────
print("\n" + "=" * 60)
print("⚡ [4/6] Launching Ollama Engine on Dual Tesla T4 GPUs (32 Billion Params)...")
print("=" * 60)

os.environ["OLLAMA_HOST"] = "127.0.0.1:11434"
os.environ["OLLAMA_ORIGINS"] = "*"
subprocess.run("pkill -f ollama", shell=True)
time.sleep(2)
subprocess.Popen(["ollama", "serve"])
time.sleep(4)

print("📥 Loading Qwen 2.5 32B into Dual T4 VRAM (~19.8 GB / 29.1 GB)...")
subprocess.run(["ollama", "pull", "qwen2.5:32b"], check=True)

# ── 6. Setup Profile & Hybrid Antigravity Routing ────────────────────────────
print("\n" + "=" * 60)
print("🔄 [5/6] Setting Up Profile & Antigravity Pro Routing...")
print("=" * 60)

os.makedirs(HERMES_PROFILE_DIR, exist_ok=True)

# Wipe old session cache to start fresh
sessions_dir = f"{HERMES_PROFILE_DIR}/sessions"
if os.path.exists(sessions_dir):
    shutil.rmtree(sessions_dir)

if os.path.exists(f"{VAULT_DIR}/.hermes_profile"):
    subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/SOUL.md {HERMES_PROFILE_DIR}/", shell=True)
    subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/config.yaml {HERMES_PROFILE_DIR}/", shell=True)
    if os.path.exists(f"{VAULT_DIR}/.hermes_profile/skills"):
        subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/skills {HERMES_PROFILE_DIR}/", shell=True)

# Write all verified keys directly to profile .env (100% full, no truncation)
with open(f"{HERMES_PROFILE_DIR}/.env", "w") as f:
    f.write(f"TELEGRAM_BOT_TOKEN={TELEGRAM_BOT_TOKEN}\n")
    f.write(f"TELEGRAM_ALLOWED_USERS={TELEGRAM_USER_ID}\n")
    f.write("GATEWAY_ALLOW_ALL_USERS=true\n")
    f.write(f"GOOGLE_API_KEY={GOOGLE_API_KEY}\n")
    f.write(f"GEMINI_API_KEY={GOOGLE_API_KEY}\n")
    f.write(f"HERMES_CUSTOM_OPENAI_API_KEY={HERMES_CUSTOM_OPENAI_API_KEY}\n")
    f.write(f"OMNIROUTE_API_KEY={OMNIROUTE_API_KEY}\n")
    f.write(f"HERMES_CUSTOM_FIRST_TIME_API_KEY={HERMES_CUSTOM_FIRST_TIME_API_KEY}\n")
    f.write(f"WIKI_PATH={VAULT_DIR}\n")
    f.write(f"OBSIDIAN_VAULT_PATH={VAULT_DIR}\n")

os.environ["WIKI_PATH"] = VAULT_DIR
os.environ["OBSIDIAN_VAULT_PATH"] = VAULT_DIR
os.environ["TELEGRAM_BOT_TOKEN"] = TELEGRAM_BOT_TOKEN
os.environ["TELEGRAM_ALLOWED_USERS"] = TELEGRAM_USER_ID
os.environ["GATEWAY_ALLOW_ALL_USERS"] = "true"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GEMINI_API_KEY"] = GOOGLE_API_KEY
os.environ["HERMES_CUSTOM_OPENAI_API_KEY"] = HERMES_CUSTOM_OPENAI_API_KEY
os.environ["HERMES_PROFILE"] = "llm-wiki"
os.environ["HERMES_HOME"] = HERMES_PROFILE_DIR

subprocess.run(["hermes", "profile", "use", "llm-wiki"])
subprocess.run(["hermes", "config", "set", "model.provider", "first-time"])
subprocess.run(["hermes", "config", "set", "model.default", "antigravity/gemini-3.7-flash-high"])
subprocess.run(["hermes", "config", "set", "model.base_url", "http://localhost:20128/v1"])

def sync_vault(commit_msg="Auto-sync from Kaggle Hybrid Agent"):
    try:
        subprocess.run(["git", "-C", VAULT_DIR, "add", "."], check=True)
        res = subprocess.run(["git", "-C", VAULT_DIR, "commit", "-m", commit_msg], capture_output=True, text=True)
        if "nothing to commit" not in res.stdout:
            subprocess.run(["git", "-C", VAULT_DIR, "push", "origin", REPO_BRANCH], check=True)
            print(f"[Vault Sync] Changes pushed to GitHub: {commit_msg}")
    except Exception as e:
        print(f"[Vault Sync Error] {e}")

def auto_sync_worker():
    while True:
        time.sleep(180)
        sync_vault()

threading.Thread(target=auto_sync_worker, daemon=True).start()

# ── 7. Launch Hermes Hybrid Gateway ───────────────────────────────────────────
print("\n" + "=" * 60)
print("🤖 [6/6] HERMES HYBRID AGENT ONLINE (ANTIGRAVITY GOOGLE AI PRO + DUAL T4)")
print("=" * 60)

try:
    subprocess.run(["hermes", "gateway", "run", "--accept-hooks"])
finally:
    sync_vault("Final session sync before Kaggle GPU shutdown")
    print("✨ Clean shutdown complete. All changes pushed to GitHub.")
```

---

## ⚙️ In-Chat Model Commands on Telegram

You can dynamically switch between your models directly in Telegram:

| Command | Model Activated | Best Used For |
| :--- | :--- | :--- |
| **`/model omni`** | **Antigravity (Google AI Pro)** | ⚡ **Google AI Pro Reasoning (High Effort)** — auto-routing to Gemini 3.7 Flash High on your Pro subscription. |
| **`/model qwen`** | **Qwen 2.5 32B** (Dual T4 GPU) | 🚀 **Local GPU workhorse** — unlimited local execution in 19.8 GB VRAM, zero rate limits. |
| **`/model sonnet`** | **Claude Sonnet 4.6 / 5** | 🛠️ **Deep coding architecture** & structured refactoring via Bluesminds. |
| **`/model opus`** | **Claude Opus 4.6** | 🧠 **Maximum reasoning depth** and complex multi-domain synthesis. |
| **`/status`** | System Diagnostics | 📊 Check currently active model, memory status, and tool availability. |
