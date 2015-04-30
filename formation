# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
#----------------------------------------------------------
# Categories
#----------------------------------------------------------


class formation_categorie(osv.osv):

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _name = "formation.categorie"
    _description = u"Catégorie"
    _columns = {
        'name': fields.char('Nom', required=True, translate=True, select=True),
        'active': fields.boolean('Active'),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Nom'),
        'parent_id': fields.many2one('formation.categorie',u'catégorie parent', select=True, ondelete='cascade'),
        'child_id': fields.one2many('formation.categorie', 'parent_id', string=u'Catégorie associée'),
        'sequence': fields.integer(u'Séquence', select=True ),
        'type': fields.selection([('view','Vue'), ('normal',u'Catégorie')], u'Type de catégorie' ),
        'parent_left': fields.integer('Left Parent', select=1),
        'parent_right': fields.integer('Right Parent', select=1),
      }


    _defaults = {
        'type' : 'normal',
        'active': 1,
    }

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence, name'
    _order = 'parent_left'

    _constraints = [
        (osv.osv._check_recursion, u'Création récursive imposible ', ['parent_id'])
    ]



formation_categorie()

class formation_savoir(osv.osv):


    _name = "formation.savoir"
    _description = u"Savoir"
    _columns = {
        'name': fields.char('Nom', required=True,  select=True),
        'active': fields.boolean('Active'),
        'type': fields.selection([('savoir',u'Connaissance'), ('faire',u'Savoir-Faire'), ('etre',u'Savoir-Etre') ], u'Type de savoir'  ,                       required=True ),

    }
    _defaults = {

        'active': 1,
    }

formation_savoir()


class formation_competence(osv.osv):

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _name = "formation.competence"
    _description = u"Compétence"
    _columns = {
        'name': fields.char('Nom', required=True, translate=True, select=True),
        'active': fields.boolean('Active'),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Nom'),
        'parent_id': fields.many2one('formation.competence',u'compétence parent', select=True, ondelete='cascade'),
        'child_id': fields.one2many('formation.competence', 'parent_id', string=u'Compétence associée'),
        'sequence': fields.integer(u'Séquence', select=True ),
        'type': fields.selection([('view','Vue'), ('normal',u'Compétence')], u'Type de compétence' ),
        'parent_left': fields.integer('Left Parent', select=1),
        'parent_right': fields.integer('Right Parent', select=1),
        'savoir_id': fields.many2many('formation.savoir', 'formation_savoir_rel', 'competence_id', 'savoir_id', u'Savoirs associés'),
    }


    _defaults = {
        'type' : 'normal',
        'active': 1,
    }

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence, name'
    _order = 'parent_left'

    _constraints = [
        (osv.osv._check_recursion, u'Création récursive imposible ', ['parent_id'])
    ]



formation_competence()




class formation(osv.osv):
    _name = 'formation'



    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):

        if context is None:
            context = {}
        option_user = self.pool.get('ir.values').get_default(cr, uid, 'formation', 'option_user') 
        option_groupe = self.pool.get('ir.values').get_default(cr, uid, 'formation', 'option_groupe') 
        option_pre_requis = self.pool.get('ir.values').get_default(cr, uid, 'formation', 'option_pre_requis') 


        formation_user_obj = self.pool.get('formation.user')
        groupe_obj = self.pool.get('res.groups')
        formation_groupe_obj = self.pool.get('formation.groupe')

        groupe_user = groupe_obj.search(cr, uid, [
                                             ('users','=',uid)], 
                                              context=context)

 #       args.append((('formation_groupe.groupe_id', 'in', groupe)))

        liste = super(formation, self).search(cr, uid, args, offset=offset, limit=limit, order=order, context=context, count=count) 
        resultat = []
###     user admin 
        if uid == 1 :
           return liste

######  gestion des inscrits

        I = 0 
        if liste and  option_user :
             # traitement d'une ligne de formation  
             for line in self.browse(cr, uid, liste, context=context):
                 # verification  presence dans la liste 
                 if len(line.formation_user) > 0 :
                     # recherche utlisateur  
                     groupe_ok = False
                     for line_group in line.formation_user :
                          # verification utilisateur 
                          if line_group.user_id.id  == uid :
                              groupe_ok = True

                     if groupe_ok == True :
                          
                          resultat.append(liste[I])
                # formation sans user
                # else:
                #     resultat.append(liste[I])
                 I = I + 1
        else:
            resultat = liste 

        liste = resultat
######  gestion des groupes
        resultat = []

        I = 0 
        if liste and option_groupe :
             # traitement d'une ligne de formation  
             for line in self.browse(cr, uid, liste, context=context):
                 # si un groupe ou plus est associe
                 if len(line.formation_groupe) > 0 :
                     # recherche du groupe 
                     groupe_ok = False
                     for line_group in line.formation_groupe :
                          # verification du groupe
                          if line_group.groupe_id.id in groupe_user :
                              groupe_ok = True

                     if groupe_ok == True :
                          
                          resultat.append(liste[I])
                # formation sans groupe
                # else:
                #     resultat.append(liste[I])
                 I = I + 1
        else:
            resultat = liste 


##### gestion pre requis

        resultat2 = []
        I = 0 
        
        if resultat and option_pre_requis :  

             for line in self.browse(cr, uid, resultat, context=context):
                 # DEBUT traitement ligne de formation 

                 if len(line.formation_prerequis) > 0 :
               #  if line.formation_prerequis:

                    for line2 in line.formation_prerequis :
                         # DEBUT traitement ligne formation pre requis

                         niveau = 0
                         groupe_ok = True

                         if line2.prerequis_id.formation_groupe and option_groupe: 

                             for line_group in line2.prerequis_id.formation_groupe :

                                 # DEBUT traitement ligne groupe formation pre requis
                                 # recherche du groupe 
                                 groupe_ok = False
                                 # verification du groupe 

                                 if line_group.groupe_id.id in groupe_user :

                                          if line2.prerequis_id.niveau_actuel >= line_group.niveau_necessaire :
                                               groupe_ok = True
                   
                                 # FIN traitement ligne groupe formation pre requis
                         if line2.prerequis_id.formation_user and option_user : 
                             groupe_ok = False
                             for line_user in line2.prerequis_id.formation_user :

                                  # DEBUT traitement ligne user formation pre requis

                                  if line_user.user_id.id == uid :

                                      if line2.prerequis_id.niveau_actuel >= line_user.niveau_necessaire :
                                            groupe_ok = True

                                 # FIN traitement ligne user formation pre requis

                         if line2.prerequis_id.niveau_actuel < line2.niveau_necessaire :
                                            groupe_ok = False
                     
                           
                         if groupe_ok == True :
                                  resultat2.append(resultat[I])

                         # FIN traitement ligne formation pre requis
                 else:

                    resultat2.append(resultat[I])
                 I = I + 1
                 # FIN  traitement ligne de formation 

        else:
            resultat2 = resultat

        return resultat2        



    def _niveau_actuel(self, cr, uid, ids, field_name, arg, context=None):

        res = {}

        if context is None:
            context = {}
        formation_user_obj = self.pool.get('formation.user')

        I = 0 
        for line in self.browse(cr, uid, ids, context=context):

           res[line.id] = 0 
          
           niveau = formation_user_obj.search(cr, uid, [('formation_id','=',ids[I]),
                                             ('user_id','=',uid)], 
                                              context=context)
           
           I = I + 1 
           if niveau :   
               ligne = formation_user_obj.browse(cr, uid, niveau, context=context)

               res[line.id] = ligne[0].niveau_actuel
        return res

    def _niveau_necessaire(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        formation_user_obj = self.pool.get('formation.user')
        I= 0
        for line in self.browse(cr, uid, ids, context=context):
           res[line.id] = 0 
           niveau = formation_user_obj.search(cr, uid, [('formation_id','=',ids[I]),
                                             ('user_id','=',uid)], 
                                              context=context)
           I = I + 1 
           if niveau :   
               ligne = formation_user_obj.browse(cr, uid, niveau, context=context)

               res[line.id] = ligne[0].niveau_necessaire
        return res



    def _niveau_objectif(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        formation_groupe_obj = self.pool.get('formation.groupe')
        I= 0
        for line in self.browse(cr, uid, ids, context=context):
           res[line.id] = 0 
           niveau = formation_groupe_obj.search(cr, uid, [('formation_id','=',ids[I])
                                                         ], 
                                                         context=context)
           I = I + 1 

           if niveau :   

               for ligne in  formation_groupe_obj.browse(cr, uid, niveau, context=context):

                   if ligne.niveau_necessaire > res[line.id]:
                        res[line.id] = ligne.niveau_necessaire
        return res


    def _get_default_company(self, cr, uid, context=None):
        company_id = self.pool.get('res.users')._get_company(cr, uid, context=context)
        if not company_id:
            raise osv.except_osv(_('Error!'), _('There is no default company for the current user!'))
        return company_id

    def maj_session_plus(self, cr, uid, ids, context=None):
        '''
        modification information session pour un utilisateur ajout un point 
        '''
        formation_user_obj = self.pool.get('formation.user')

        # date du jour
        dt_j =        fields.date.context_today(self, cr, uid, context=context)


        for formation  in self.browse(cr, uid, ids, context=context):

            user = formation_user_obj.search(cr, uid, [('formation_id','=',formation.id),
                                             ('user_id','=',uid)], 
                                              context=context)
       
            if user : 

               user_ligne = formation_user_obj.browse(cr, uid, user, context=context)

               niveau = user_ligne[0].niveau_actuel

               if niveau < 10 :
                   niveau = niveau  +1 

               maj = formation_user_obj.write(cr, uid, user, {'niveau_actuel':niveau,'date_cours':dt_j}, context=None)
            else:
               niveau = 0
               maj = formation_user_obj.create(cr, uid, {'user_id':uid,'niveau_actuel':niveau,'date_cours':dt_j, 'formation_id':formation.id}, context=None)


   
        return True

    def maj_session_moins(self, cr, uid, ids, context=None):
        '''
        modification information session pour un utilisateur moins  un point 
        '''

        formation_user_obj = self.pool.get('formation.user')

        # date du jour
        dt_j =        fields.date.context_today(self, cr, uid, context=context)


        for formation  in self.browse(cr, uid, ids, context=context):

            user = formation_user_obj.search(cr, uid, [('formation_id','=',formation.id),
                                             ('user_id','=',uid)], 
                                              context=context)
       
            if user : 

               user_ligne = formation_user_obj.browse(cr, uid, user, context=context)

               niveau = user_ligne[0].niveau_actuel

               if niveau > 0  :
                   niveau = niveau  - 1

               maj = formation_user_obj.write(cr, uid, user, {'niveau_actuel':niveau,'date_cours':dt_j}, context=None)
            else:
               niveau = 0
               maj = formation_user_obj.create(cr, uid, {'user_id':uid,'niveau_actuel':niveau,'date_cours':dt_j, 'formation_id':formation.id}, context=None)

   
        return True


 
    _columns = {

        # nom  de la formation 
        'name': fields.char('Formation', size=64, required=True),
        'active': fields.boolean('Active'),
        'version': fields.char('Version', size=10),
        'formation_user': fields.one2many('formation.user', 'formation_id', 'Suivi utilisateur'),
        'formation_groupe': fields.one2many('formation.groupe', 'formation_id', 'Ojectif groupe'),
        'formation_prerequis': fields.one2many('formation.prerequis', 'formation_id', u'pré-requis '),
         ### non utilise 
        #'pre_requis_ids' : fields.many2many("formation", "pre_requis_formation", "pre_requis_id", "formation_id", u"liste des pré-requis "),
         ###
        'contenu': fields.text("Contenu"),

        'niveau_actuel': fields.function(_niveau_actuel, string=u'Niveau actuel', help=u"Estimation de votre niveau niveau actuel.( 1 à 10)"),
        'niveau_necessaire': fields.function(_niveau_necessaire, string=u'Niveau nécessaire', help=u"Niveau optimum en fonction de l'activité quotidienne. ( 1 à 10)"),
        'niveau_objectif': fields.function(_niveau_objectif, string=u'Niveau Minimum', help=u"Niveau minimum à avoir.( 1 à 10)"),
        'duree_vie': fields.integer(u'Durée de vie', help=u"Durée de vie de la compétence acquise (en jours)"),
        'renforcement': fields.integer(u'Durée de  reforcement', help=u"Durée de renforcement (en jours)"),
        'a_refaire' : fields.boolean('A refaire ', help=u"Une nouvelle version nécessite de refaire le parcours"),
        'valide' : fields.boolean('Formation validée ', help=u"La formation a été vérifiée et approuvée"),
        'auteur' : fields.many2one('res.users', 'Auteur'),
        'relecteur' :fields.many2one('res.users', 'Relecteur'),
        'confirmation' : fields.boolean('Confirmation nécessaire', help=u"Confirmation du niveau nécessaire"),

        'company_id': fields.many2one('res.company', 'Company'),
        'categorie_id': fields.many2one('formation.categorie', u'Catégorie'),
       'competence_ids': fields.many2many('formation.competence', 'formation_competence_rel', 'formation_id', 'competence_id', u'Compétences associées'),



      }

    _defaults = {
        'active': 1,
        'company_id': _get_default_company,
        
    }

formation()



class formation_user(osv.osv):
    _name = 'formation.user'


 
    _columns = {
        'formation_id': fields.many2one('formation', 'Formation', required=True, ondelete='cascade', select=True ),
        # lien utilisateur
        'user_id':fields.many2one('res.users', 'Utilisateur', required=True ),
        # niveau utilisateur
        'niveau_actuel': fields.integer(u'Niveau actuel', help=u"Estimation niveau actuel.( 1 à 10)"),
        'niveau_necessaire': fields.integer(u'Niveau nécessaire', help=u"Estimation niveau nécessaire.( 1 à 10)"),
        'duree_vie': fields.integer(u'Durée de vie', help=u"Durée de vie de la compétence acquise (en jours)"),
        'renforcement': fields.integer(u'Durée de  renforcement', help=u"Durée de renforcement (en jours)"),
        'renforcement_niveau_1': fields.integer(u'Renforcement du niveau ', help=u"Renforcement du niveau 1 (en jours)"),
        'renforcement_niveau_2': fields.integer(u'Renforcement du niveau ', help=u"Renforcement du niveau 2 (en jours)"),
        'renforcement_niveau_3': fields.integer(u'Renforcement du niveau ', help=u"Renforcement du niveau 3 (en jours)"),
        'renforcement_niveau_4': fields.integer(u'Renforcement du niveau ', help=u"Renforcement du niveau 4 (en jours)"),
        'renforcement_niveau_5': fields.integer(u'Renforcement du niveau ', help=u"Renforcement du niveau 5 (en jours)"),
        'renforcement_niveau_6': fields.integer(u'Renforcement du niveau ', help=u"Renforcement du niveau 6 (en jours)"),
        'renforcement_niveau_7': fields.integer(u'Renforcement du niveau ', help=u"Renforcement du niveau 7 (en jours)"),
        'renforcement_niveau_8': fields.integer(u'Renforcement du niveau ', help=u"Renforcement du niveau 8 (en jours)"),
        'renforcement_niveau_9': fields.integer(u'Renforcement du niveau ', help=u"Renforcement du niveau 9 (en jours)"),
        'renforcement_niveau_10': fields.integer(u'Renforcement du niveau ', help=u"Renforcement du niveau 10 (en jours)"),
        'date_cours': fields.date('Date dernier parcours' ),
        'date_niveau_1': fields.date('Date passage niveau 1' ),
        'date_niveau_2': fields.date('Date passage niveau 2' ),
        'date_niveau_3': fields.date('Date passage niveau 3' ),
        'date_niveau_4': fields.date('Date passage niveau 4' ),
        'date_niveau_5': fields.date('Date passage niveau 5' ),
        'date_niveau_6': fields.date('Date passage niveau 6' ),
        'date_niveau_7': fields.date('Date passage niveau 7' ),
        'date_niveau_8': fields.date('Date passage niveau 8' ),
        'date_niveau_9': fields.date('Date passage niveau 9' ),
        'date_niveau_10': fields.date('Date passage niveau 10' ),





      }
    _defaults = {
        'date_cours': fields.date.context_today,
      }

formation_user()

class formation_groupe(osv.osv):
    _name = 'formation.groupe'


 
    _columns = {
        'formation_id': fields.many2one('formation', 'Formation', required=True, ondelete='cascade', select=True ),
        # lien groupe
        'groupe_id':fields.many2one('res.groups', 'Groupe', required=True ),
        # niveau utilisateur
        'niveau_necessaire': fields.integer(u'Niveau nécessaire', help=u"Estimation niveau nécessaire.( 1 à 10)"),



      }


formation_groupe()

class formation_prerequis(osv.osv):
    _name = 'formation.prerequis'


 
    _columns = {
        'formation_id': fields.many2one('formation', 'Formation', required=True, ondelete='cascade', select=True ),
        # lien formation
        'prerequis_id': fields.many2one('formation', 'Formation', required=True, ondelete='cascade', select=True ),
        # niveau utilisateur
        'niveau_necessaire': fields.integer(u'Niveau nécessaire', help=u"Niveau nécessaire.( 1 à 10)"),



      }


formation_prerequis()


