# -*- coding: utf-8 -*-
##############################################################################
#
#    
#    Copyright (C) 2015 Lispro
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
{
        "name" : "formation",
        "version" : "08042015",
        "author" : "lispro",
        "website" : "http://www.le-savoir-libre.fr",
        "category" : "Vertical Modules/Parametrization",
        "description": """ module formation FCL
                            """,
        "depends" : [ "base", ],

        "init_xml" : [ ],
        "demo_xml" : [ ],
        "data" : [

                        "security/security.xml",
                        "security/ir.model.access.csv",
                        "configuration_view.xml",
                        'formation_view.xml',

                        ],
        "installable": True
} 
