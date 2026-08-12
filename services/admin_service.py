from typing import Dict, Any, List
import datetime
from database.database import execute_query
from utils.timezone import format_kolkata_time
from utils.security import sanitize_user_dict_for_admin

def get_admin_kpi_metrics() -> Dict[str, int]:
    """
    Calculates executive KPI card metrics directly from MySQL/SQLite.
    - Total Users
    - Today's Registrations
    - Total Logins
    - Today's Logins
    - Total Resumes
    - Total Resume Analyses
    - Total Job Matches
    - Active Users
    """
    total_users = 0
    today_users = 0
    total_logins = 0
    today_logins = 0
    total_resumes = 0
    total_analyses = 0
    total_job_matches = 0
    active_users = 0

    try:
        res = execute_query("SELECT COUNT(id) as cnt FROM users", fetchone=True)
        if res:
            total_users = res.get("cnt", 0)
    except Exception:
        pass

    try:
        res = execute_query("SELECT COUNT(id) as cnt FROM users WHERE DATE(created_at) = DATE('now')", fetchone=True)
        if not res or res.get("cnt") == 0:
            res = execute_query("SELECT COUNT(id) as cnt FROM users WHERE DATE(created_at) = CURRENT_DATE", fetchone=True)
        if res:
            today_users = res.get("cnt", 0)
    except Exception:
        pass

    try:
        res = execute_query("SELECT COUNT(login_id) as cnt FROM login_activity WHERE login_status = 'SUCCESS'", fetchone=True)
        if res:
            total_logins = res.get("cnt", 0)
        else:
            res_act = execute_query("SELECT COUNT(id) as cnt FROM activity_logs WHERE action = 'LOGIN'", fetchone=True)
            if res_act:
                total_logins = res_act.get("cnt", 0)
    except Exception:
        pass

    try:
        res = execute_query("SELECT COUNT(login_id) as cnt FROM login_activity WHERE DATE(login_time) = DATE('now')", fetchone=True)
        if not res or res.get("cnt") == 0:
            res = execute_query("SELECT COUNT(login_id) as cnt FROM login_activity WHERE DATE(login_time) = CURRENT_DATE", fetchone=True)
        if res:
            today_logins = res.get("cnt", 0)
    except Exception:
        pass

    try:
        res = execute_query("SELECT COUNT(id) as cnt FROM resumes", fetchone=True)
        if res:
            total_resumes = res.get("cnt", 0)
    except Exception:
        pass

    try:
        res = execute_query("SELECT COUNT(id) as cnt FROM resume_analysis", fetchone=True)
        if res:
            total_analyses = res.get("cnt", 0)
    except Exception:
        pass

    try:
        res = execute_query("SELECT COUNT(id) as cnt FROM job_matching", fetchone=True)
        if res:
            total_job_matches = res.get("cnt", 0)
    except Exception:
        pass

    try:
        res = execute_query("SELECT COUNT(DISTINCT user_id) as cnt FROM activity_logs", fetchone=True)
        if res:
            active_users = res.get("cnt", 0)
    except Exception:
        pass

    return {
        "total_users": max(total_users, 1),
        "today_users": today_users,
        "total_logins": max(total_logins, 1),
        "today_logins": today_logins,
        "total_resumes": total_resumes,
        "total_analyses": total_analyses,
        "total_job_matches": total_job_matches,
        "active_users": max(active_users, 1)
    }


def get_admin_users_list(search_query: str = "", date_filter: str = "All", resume_filter: str = "All") -> List[Dict[str, Any]]:
    """
    Fetches user table records for admin display.
    SECURITY GUARANTEE: Explicitly SELECTS only safe columns and scrubs password/hash fields completely.
    """
    sql = """
    SELECT 
        u.id as user_id,
        u.full_name,
        u.email,
        u.mobile,
        u.role,
        u.created_at as registered_date,
        (SELECT MAX(login_time) FROM login_activity WHERE user_id = u.id) as last_login,
        (SELECT COUNT(login_id) FROM login_activity WHERE user_id = u.id) as login_count,
        (SELECT status FROM resumes WHERE user_id = u.id ORDER BY is_active DESC, uploaded_at DESC LIMIT 1) as resume_status,
        (SELECT filename FROM resumes WHERE user_id = u.id ORDER BY is_active DESC, uploaded_at DESC LIMIT 1) as resume_name,
        (SELECT MAX(created_at) FROM activity_logs WHERE user_id = u.id) as last_activity
    FROM users u
    ORDER BY u.created_at DESC
    """
    
    users = execute_query(sql, fetchall=True) or []
    
    formatted = []
    for u in users:
        # Scrub passwords just in case
        u_clean = sanitize_user_dict_for_admin(u)
        
        name = u_clean.get("full_name") or "User"
        email = u_clean.get("email") or ""
        
        # Apply Search Filter
        if search_query:
            sq = search_query.lower().strip()
            if sq not in name.lower() and sq not in email.lower():
                continue
                
        r_status = u_clean.get("resume_status") or "No Resume"
        if resume_filter != "All":
            if resume_filter == "With Active Resume" and "Active" not in r_status:
                continue
            elif resume_filter == "No Resume" and "No Resume" not in r_status:
                continue

        formatted.append({
            "user_id": u_clean.get("user_id"),
            "full_name": name,
            "email": email,
            "mobile": u_clean.get("mobile") or "N/A",
            "role": u_clean.get("role") or "user",
            "registered_date": format_kolkata_time(u_clean.get("registered_date")),
            "last_login": format_kolkata_time(u_clean.get("last_login")) if u_clean.get("last_login") else "Never",
            "login_count": u_clean.get("login_count") or 0,
            "resume_status": r_status,
            "resume_name": u_clean.get("resume_name") or "None",
            "last_activity": format_kolkata_time(u_clean.get("last_activity")) if u_clean.get("last_activity") else "None"
        })
        
    return formatted


def get_login_activity_logs(limit: int = 25) -> List[Dict[str, Any]]:
    """
    Fetches login activity records joining users table.
    SECURITY GUARANTEE: Excludes passwords completely.
    """
    sql = """
    SELECT 
        l.login_id,
        l.user_id,
        u.full_name,
        u.email,
        l.login_time,
        l.logout_time,
        l.login_status,
        l.session_id,
        l.ip_address
    FROM login_activity l
    JOIN users u ON l.user_id = u.id
    ORDER BY l.login_time DESC
    LIMIT %s
    """
    logs = execute_query(sql, (limit,), fetchall=True) or []
    
    res = []
    for log in logs:
        clean = sanitize_user_dict_for_admin(log)
        res.append({
            "login_id": clean.get("login_id"),
            "user_id": clean.get("user_id"),
            "full_name": clean.get("full_name"),
            "email": clean.get("email"),
            "login_time": format_kolkata_time(clean.get("login_time")),
            "logout_time": format_kolkata_time(clean.get("logout_time")) if clean.get("logout_time") else "Active Session",
            "login_status": clean.get("login_status", "SUCCESS"),
            "session_id": clean.get("session_id", "N/A"),
            "ip_address": clean.get("ip_address", "127.0.0.1")
        })
    return res


def get_resume_activity_logs(limit: int = 25) -> List[Dict[str, Any]]:
    """
    Fetches resume uploads, view events, and replacements from activity_logs.
    """
    sql = """
    SELECT 
        a.id as log_id,
        a.user_id,
        u.full_name,
        u.email,
        a.action,
        a.details,
        a.created_at
    FROM activity_logs a
    JOIN users u ON a.user_id = u.id
    WHERE a.action LIKE 'RESUME%%' OR a.action LIKE 'ATS%%'
    ORDER BY a.created_at DESC
    LIMIT %s
    """
    logs = execute_query(sql, (limit,), fetchall=True) or []
    
    formatted = []
    for l in logs:
        clean = sanitize_user_dict_for_admin(l)
        formatted.append({
            "log_id": clean.get("log_id"),
            "user_id": clean.get("user_id"),
            "full_name": clean.get("full_name"),
            "email": clean.get("email"),
            "action": clean.get("action"),
            "details": clean.get("details"),
            "timestamp": format_kolkata_time(clean.get("created_at"))
        })
    return formatted


def get_resume_analysis_monitoring(limit: int = 25) -> List[Dict[str, Any]]:
    """
    Fetches resume analysis records for admin inspection.
    """
    sql = """
    SELECT 
        ra.id as analysis_id,
        ra.user_id,
        u.full_name,
        u.email,
        r.filename as resume_name,
        ra.resume_score,
        ra.ats_score,
        ra.resume_quality,
        ra.analyzed_at
    FROM resume_analysis ra
    JOIN users u ON ra.user_id = u.id
    LEFT JOIN resumes r ON ra.resume_id = r.id
    ORDER BY ra.analyzed_at DESC
    LIMIT %s
    """
    records = execute_query(sql, (limit,), fetchall=True) or []
    
    res = []
    for r in records:
        clean = sanitize_user_dict_for_admin(r)
        res.append({
            "analysis_id": clean.get("analysis_id"),
            "user_id": clean.get("user_id"),
            "full_name": clean.get("full_name"),
            "email": clean.get("email"),
            "resume_name": clean.get("resume_name") or "Active Resume.pdf",
            "resume_score": clean.get("resume_score", 85),
            "ats_score": clean.get("ats_score", 88),
            "resume_quality": clean.get("resume_quality", "Good"),
            "analyzed_at": format_kolkata_time(clean.get("analyzed_at"))
        })
    return res


def get_user_activity_timeline(user_id: int = None, limit: int = 30) -> List[Dict[str, Any]]:
    """
    Fetches activity logs timeline for a specific user or system-wide.
    """
    if user_id:
        sql = """
        SELECT a.id, a.user_id, u.full_name, u.email, a.action, a.details, a.created_at
        FROM activity_logs a
        JOIN users u ON a.user_id = u.id
        WHERE a.user_id = %s
        ORDER BY a.created_at DESC
        LIMIT %s
        """
        logs = execute_query(sql, (user_id, limit), fetchall=True) or []
    else:
        sql = """
        SELECT a.id, a.user_id, u.full_name, u.email, a.action, a.details, a.created_at
        FROM activity_logs a
        JOIN users u ON a.user_id = u.id
        ORDER BY a.created_at DESC
        LIMIT %s
        """
        logs = execute_query(sql, (limit,), fetchall=True) or []

    timeline = []
    for l in logs:
        clean = sanitize_user_dict_for_admin(l)
        timeline.append({
            "id": clean.get("id"),
            "user_id": clean.get("user_id"),
            "full_name": clean.get("full_name"),
            "email": clean.get("email"),
            "action": clean.get("action"),
            "details": clean.get("details"),
            "timestamp": format_kolkata_time(clean.get("created_at"))
        })
    return timeline


def get_detailed_user_inspector(user_id: int) -> Dict[str, Any]:
    """
    Compiles complete candidate user inspector for admin detail modal.
    SECURITY GUARANTEE: Excludes passwords completely.
    """
    if not user_id:
        return {}

    user_raw = execute_query("SELECT id, full_name, email, mobile, age, role, created_at FROM users WHERE id = %s", (user_id,), fetchone=True) or {}
    user_clean = sanitize_user_dict_for_admin(user_raw)
    
    profile = execute_query("SELECT * FROM profiles WHERE user_id = %s", (user_id,), fetchone=True) or {}
    resumes = execute_query("SELECT id, filename, file_type, file_size, version, is_active, resume_score, ats_score, uploaded_at FROM resumes WHERE user_id = %s", (user_id,), fetchall=True) or []
    latest_analysis = execute_query("SELECT * FROM resume_analysis WHERE user_id = %s ORDER BY analyzed_at DESC LIMIT 1", (user_id,), fetchone=True) or {}
    job_matches = execute_query("SELECT job_title, company, match_percentage FROM job_matching WHERE user_id = %s ORDER BY match_percentage DESC LIMIT 3", (user_id,), fetchall=True) or []
    user_timeline = get_user_activity_timeline(user_id, limit=15)

    return {
        "user_id": user_clean.get("id"),
        "full_name": user_clean.get("full_name"),
        "email": user_clean.get("email"),
        "mobile": user_clean.get("mobile"),
        "age": user_clean.get("age"),
        "role": user_clean.get("role", "user"),
        "registered_at": format_kolkata_time(user_clean.get("created_at")),
        "profile": profile,
        "resumes": resumes,
        "latest_analysis": latest_analysis,
        "job_matches": job_matches,
        "timeline": user_timeline
    }
