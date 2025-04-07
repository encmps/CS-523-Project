import os
from copy import deepcopy

template_symbol = {
    'aaa_cartesion/applications/astronomy_shop.pytemplate': ['$inject_otel$', '$OtelFaultInjector$'],
    'aaa_cartesion/applications/hotel_res.pytemplate': ['$inject_app$', '$ApplicationFaultInjector$'],
    'aaa_cartesion/applications/social_net.pytemplate': ['$inject_virtual$', '$VirtualizationFaultInjector$']
}

injector_to_class = {
    'inject_corrupt_configuration_file': 'ConfigFileFaultInjector',
    'inject_database_connection_timeout': 'DatabaseConnectionTimeoutInjector',
    'inject_disk_full': 'DiskFullInjector',
    'inject_dns_resolution_failure': 'DNSResolutionFaultInjector',
    'inject_high_cpu_utilization': 'HighCPUUtilizationInjector'
}

def assenble_problem(template_name: str):
    template_mark = template_name.replace('aaa_cartesion/applications/', '').replace('.pytemplate', '')
    with open(template_name) as f:
        template = f.read()
    for k, v in injector_to_class.items():
        cur_template = deepcopy(template)
        cur_template = cur_template.replace(
            template_symbol[template_name][0], k
        ).replace(
            template_symbol[template_name][1], v
        )
        with open(f'aaa_cartesion/cartesian_result/{k}_{template_mark}.py', 'w') as f:
            f.write(cur_template)

if __name__ == '__main__':
    for template_name in template_symbol:
        assenble_problem(template_name)