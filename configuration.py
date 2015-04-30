# -*- coding: utf-8 -*-
##############################################################################
#
#    
#    Copyright (C) Lispro 2015
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""

"""

from openerp.osv import fields, osv

class res_config_settings(osv.osv_memory):
    _inherit = 'res.config.settings'

    _columns = {
        'default_option_user': fields.boolean(u"gestion des inscriptions utlisateur", default_model='formation'),
        'default_option_groupe': fields.boolean(u"gestion des inscriptions utlisateur",  default_model='formation'),
        'default_option_pre_requis': fields.boolean(u"gestion des pré requis", default_model='formation'),
    }

res_config_settings()
