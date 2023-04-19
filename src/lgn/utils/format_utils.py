def format_time(t_hours_f):
    if t_hours_f < 0:
        return '(-' + format_time(-t_hours_f) + ')'

    t_minutes = int(round((t_hours_f % 1) * 60,0))

    if t_hours_f > 0:
        return f'{t_hours_f:,.0f}h{t_minutes:02d}m'

    return f'{t_minutes}m'

def format_distance(d_km):
    if d_km < 2:
        return f'{d_km * 1000:,.0f}m'
    return f'{d_km:,.0f}km'