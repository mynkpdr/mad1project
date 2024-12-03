def register_template_filters(app):
    @app.template_filter('indian_rupee_format')
    def indian_rupee_format(value):
        value = str(value)

        if len(value) <= 3:
            return value

        last_three = value[-3:]
        rest = value[:-3]

        rest = rest[::-1]
        rest = ','.join([rest[i:i+2] for i in range(0, len(rest), 2)])
        rest = rest[::-1]
        
        return f'{rest},{last_three}'
