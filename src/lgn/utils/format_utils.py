def format_time(t_hours_f):
    if t_hours_f < 0:
        return '(-' + format_time(-t_hours_f) + ')'

    (int)(t_hours_f / 24)
    t_hours = (int)(t_hours_f % 24)
    t_minutes = (int)((t_hours_f % 1) * 60 + 0.5)

    if t_hours > 0:
        return f'{t_hours}h{t_minutes}m'

    return f'{t_minutes}m'
