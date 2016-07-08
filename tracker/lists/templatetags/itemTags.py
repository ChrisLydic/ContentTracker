from django import template
register = template.Library()

# Computes the amount of space the offset to the percent bar should have
@register.simple_tag()
def offset( percent, *args, **kwargs ):
    return ( 1 - ( 0.01 * percent ) )

# Computes the amount of space the percent bar should have
@register.simple_tag()
def toDecimal( percent, *args, **kwargs ):
    return ( 0.01 * percent )