"""Provisioning-related forms and helper classes.

"""
from collections import OrderedDict

from cfme.fixtures import pytest_selenium as sel
from cfme.web_ui import Calendar, Form, Radio, Select, Table, Tree, tabstrip, toolbar
from cfme.web_ui.menu import nav


template_select_form = Form(
    fields=[
        ('template_table', Table('//div[@id="pre_prov_div"]/fieldset/table')),
        ('continue_button', '//img[@title="Continue"]'),
        ('cancel_button', '//img[@title="Continue"]')
    ]
)

provisioning_form = tabstrip.TabStripForm(
    fields=[
        ('submit_button', '//*[@id="form_buttons"]/li[1]/img'),
        ('cancel_button', '//*[@id="form_buttons"]/li[2]/img')
    ],
    tab_fields=OrderedDict([
        ('Request', [
            ('email', '//input[@name="requester__owner_email"]'),
            ('first_name', '//input[@id="requester__owner_first_name"]'),
            ('last_name', '//input[@id="requester__owner_last_name"]'),
            ('notes', '//textarea[@id="requester__request_notes"]'),
            ('manager_name', '//input[@id="requester__owner_manager"]'),
        ]),
        ('Purpose', [
            ('apply_tags', Tree('//div[@id="all_tags_treebox"]//table')),
        ]),
        ('Catalog', [
            ('vm_filter', Select('//select[@id="service__vm_filter"]')),
            ('catalog_name', Table('//div[@id="prov_vm_div"]/table')),
            ('num_vms', Select('//select[@id="service__number_of_vms"]')),
            ('vm_name', '//input[@name="service__vm_name"]'),
            ('vm_description', '//textarea[@id="service__vm_description"]'),
            ('provision_type', Select('//select[@id="service__provision_type"]')),
            ('linked_clone', '//input[@id="service__linked_clone"]'),
        ]),
        ('Environment', [
            ('automatic_placement', '//input[@id="environment__placement_auto"]'),
            ('datacenter', Select('//select[@id="environment__placement_dc_name"]')),
            ('cluster', Select('//select[@id="environment__placement_cluster_name"]')),
            ('resource_pool', Select('//select[@id="environment__placement_rp_name"]')),
            ('folder', Select('//select[@id="environment__placement_folder_name"]')),
            ('host_filter', Select('//select[@id="environment__host_filter"]')),
            ('host_name', Table('//div[@id="prov_host_div"]/table')),
            ('datastore_create', '//*[@id="environment__new_datastore_create"]'),
            ('datastore_filter', Select('//select[@id="environment__ds_filter"]')),
            ('datastore_name', Table('//div[@id="prov_ds_div"]/table')),
        ]),
        ('Hardware', [
            ('num_sockets', Select('//select[@id="hardware__number_of_sockets"]')),
            ('cores_per_socket', Select('//select[@id="hardware__cores_per_socket"]')),
            ('memory', Select('//select[@id="hardware__vm_memory"]')),
            ('disk_format', Radio('hardware__disk_format')),
            ('vm_limit_cpu', '//input[@id="hardware__cpu_limit"]'),
            ('vm_limit_memory', '//input[@id="hardware__memory_limit"]'),
            ('vm_reserve_cpu', '//input[@id="hardware__cpu_reserve"]'),
            ('vm_reserve_memory', '//input[@id="hardware__memory_reserve"]'),
        ]),
        ('Network', [
            ('vlan', Select('//select[@id="network__vlan"]')),
        ]),
        ('Customize', [
            ('customize_type', Select('//select[@id="customize__sysprep_enabled"]')),
            ('specification_name', Table('//div[@id="prov_vc_div"]/table')),
            ('linux_host_name', '//input[@id="customize__linux_host_name"]'),
            ('linux_domain_name', '//input[@id="customize__linux_domain_name"]'),
            ('dns_servers', '//input[@id="customize__dns_servers"]'),
            ('dns_suffixes', '//input[@id="customize__dns_suffixes"]'),
        ]),
        ('Schedule', [
            ('schedule_type', Radio('schedule__schedule_type')),
            ('provision_date', Calendar('miq_date_1')),
            ('provision_start_hour', Select('//select[@id="start_hour"]')),
            ('provision_start_min', Select('//select[@id="start_min"]')),
            ('retirement', Select('//select[@id="schedule__retirement"]')),
            ('retirement_warning', Select('//select[@id="schedule__retirement_warn"]')),
        ])
    ])
)


# Nav targets and helpers
def _nav_to_provision_form(context):
    toolbar.select('Lifecycle', 'Provision VMs')
    provider = context['provider']
    template_name = context['template_name']

    template = template_select_form.template_table.find_row_by_cells({
        'Name': template_name,
        'Provider': provider.name
    })
    if template:
        sel.click(template)
        sel.click(template_select_form.continue_button)
        return
    else:
        # Better exception?
        raise ValueError('Navigation failed: Unable to find template "%s" for provider "%s"' %
            (template_name, provider.key))

nav.add_branch('infrastructure_virtual_machines', {
    'infrastructure_provision_vms': _nav_to_provision_form
})
