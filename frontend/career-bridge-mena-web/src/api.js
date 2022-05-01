import axios from 'axios';

import { ReactSession } from 'react-client-session';

const API_BASE = "http://127.0.0.1:5000/";

export default {


    login: async (email, password, onSuccess=null, onFail=null) => {

        axios.post(
            API_BASE+"login",
            {
                email: email,
                password: password
            }
        )
        .catch(res=>{
             
            onFail()
        })
        .then(res=>{
             
            onSuccess?.(res.data)
        })
    },
    getUser: async (uid, onSuccess=null, onFail=null) => {

        axios.get(
            API_BASE+"users/"+uid,
        )
        .then(res=>{
             
            onSuccess?.(res.data)
        })
        .catch(()=>{
            ReactSession.set('user', null)
        })
    },

    USER_TYPES: {
        "Mentor": "M",
        "Seeker": "S"
    }

    ,getUserType: async (uid, onSuccess=null, onFail=null) =>{

        axios.get(
            API_BASE+"users/"+uid+"/type"
        ).then(res=>{

             
            onSuccess?.(
              res.data
           )
        }).catch(onFail)
        
    },

    

    signup: async (info, onSuccess = null, onFail = null)=>{
         

        axios.post(
            API_BASE+"users/"+info.email,
            info
        )
        .catch(res=>{
             
            onFail?.()
        })
        .then(res=>{
             

            if(info.is_seeker){
            axios.post(
                API_BASE+"seekers/"+info.email,
                {
                    sop: "",
                    open_to_work: false,
                }
            )
            .catch(res=>{
                 
                onFail?.()})
            .then(
                res2=>{
                     
                    onSuccess?.(info.email)
                }
            )
            }
            else{
                axios.post(
                    API_BASE+"mentors/"+info.email,
                    {
                        org_id: null,
                        position: null
                    }
                )
                .catch(res=>{
                     
                    onFail?.()})
                .then(
                    res2=>{
                         
                        onSuccess?.(info.email)
                    }
                )
            }
        })
        // first_name, last_name, birth_date, linkedin, website, phone, gender
    },

    setUser: async (info, onSuccess = null, onFail = null)=>{
         
            
        axios.post(
            API_BASE+"users/"+info.email,
            info
        )
        .catch(res=>{
             
            onFail?.()
        })
        .then(res=>{
             
            onSuccess?.(res.data)
        })
        // first_name, last_name, birth_date, linkedin, website, phone, gender
    },

    getCurrentPosition: async(uid, onSuccess = null, onFail = null)=>{

        axios.get(
            API_BASE+"mentors/"+uid,
        )
        .catch(onFail)
        .then(res =>{

            onSuccess?.(res.data)
        })

    },

    setCurrentPosition: async(uid, info, onSuccess = null, onFail = null)=>{
         

        axios.post(
            API_BASE+"mentors/"+uid,
            info
        )
        .catch(onFail)
        .then(res=>{
            onSuccess?.(res.data)
        })
        
        //position org_id
    },

    getAllOrganizationNames: async( onSuccess = null, onFail = null)=>{
        axios.get(
            API_BASE+"organizations/names"
        )
        .then(res=>{
            
            res.data.push({'org_name':"HARD1", 'org_id':'1'})
            res.data.push({'org_name':"HARD2", 'org_id':'2'})
            res.data.push({'org_name':"HARD3", 'org_id':'3'})
            onSuccess?.(JSON.stringify(res.data))
        })

        /*onSuccess?.([
            {'org_name':"HARD1", 'org_id':'1'},
            {'org_name':"HARD2", 'org_id':'2'},
            {'org_name':"HARD3", 'org_id':'3'}
        ])*/
    }, 

    getSeekerData: async (uid, onSuccess=null, onFail=null)=>{

        axios.get(
            API_BASE+"seekers/"+uid
        )
        .then(res=>{
            onSuccess?.(res.data)
        })
    },

    setSeekerData: async (uid, info, onSuccess=null, onFail=null)=>{

        console.log(info)
        axios.post(
            API_BASE+"seekers/"+uid,
            info
        )
        .catch(onFail)
        .then(res=>{
            onSuccess?.(res.data)
        }) 
        
        // sop, open_to_work

    },

    getEducations: async (uid, onSuccess=null, onFail=null)=>{
        
        axios.get(
            API_BASE+"users/"+uid+"/education"
        )
        .then(res=>{
            console.log(res)
            onSuccess?.(res.data)
        })

    },

    deleteEducation: async (uid, program, onSuccess=null, onFail=null)=>{
         
        
        axios.delete(
            API_BASE+"users/"+uid+"/education/"+program.id
        )
        //program id
    },

    setEducation: async (uid, program, onSuccess=null, onFail=null)=>{

        
        axios.post(
            API_BASE+"users/"+uid+"/education/"+program.id,
            program
        )
        .catch(onFail)
        .then(res=>{
            onSuccess?.(res.data)
        }) 
    },
    

    getExperiences: async (uid, onSuccess=null, onFail=null)=>{
        axios.get(
            API_BASE+"mentors/"+uid+"/experience"
        )
        .then(res=>{
            console.log(res)
            onSuccess?.(res.data)
        })
    },

    setExperience: async (uid, experience, onSuccess=null, onFail=null)=>{
        axios.post(
            API_BASE+"mentors/"+uid+"/experience/"+experience.id,
            experience  
        )
        .catch(onFail)
        .then(res=>{
            onSuccess?.(res.data)
        }) 
    },
    deleteExperience: async (uid, experience, onSuccess=null, onFail=null)=>{
        axios.delete(
            API_BASE+"mentors/"+uid+"/experience/"+experience.id
        )
    },

    getProjects: async (uid, onSuccess=null, onFail=null)=>{
        axios.get(
            API_BASE+"seekers/"+uid+"/projects"
        )
        .then(res=>{
            console.log(res)
            onSuccess?.(res.data)
        })
    },

    setProject: async (uid, project, onSuccess=null, onFail=null)=>{
         
        axios.post(
            API_BASE+"seekers/"+uid+"/projects",
            project  
        )
        .catch(onFail)
        .then(res=>{
            onSuccess?.(res.data)
        }) 
        // date and user email are keys
    },
    deleteProject: async (uid, project, onSuccess=null, onFail=null)=>{

        axios.delete(
            API_BASE+"seekers/"+uid+"/projects/delete/"+project.date
        )
    },
    getCertifications: async (uid, onSuccess=null, onFail=null)=>{
        axios.get(
            API_BASE+"seekers/"+uid+"/certifications"
        )
        .then(res=>{
            console.log(res)
            onSuccess?.(res.data)
        })
    },

    setCertification: async (uid, project, onSuccess=null, onFail=null)=>{
        axios.post(
            API_BASE+"seekers/"+uid+"/certifications",
            project  
        )
        .catch(onFail)
        .then(res=>{
            onSuccess?.(res.data)
        }) 
    },
    deleteCertification : async (uid, project, onSuccess=null, onFail=null)=>{

        axios.delete(
            API_BASE+"seekers/"+uid+"/certifications/delete?url="+project.url,  
        )
        .catch(onFail)
        .then(res=>{
            onSuccess?.(res.data)
        }) 
    },

    getSkills: async (uid, onSuccess=null, onFail=null)=>{
        axios.get(
            API_BASE+"seekers/"+uid+"/skills"
        )
        .then(res=>{
            console.log(res)
            onSuccess?.(res.data)
        })
    },

    setSkills: async (uid, skills, onSuccess=null, onFail=null)=>{
        axios.post(
            API_BASE+"seekers/"+uid+"/skills",
            skills  
        )
        .catch(onFail)
        .then(res=>{
            onSuccess?.(res.data)
        }) 
    },
    
    getFollowedFields: async (uid, onSuccess=null, onFail = null)=>{
        
        axios.get(
            API_BASE+"fields",
            {
              params: {'follower_id': uid}
            }
        )
        .then(res=>{
            console.log(res)
            onSuccess?.(res.data)
        })
    },

    unfollowField: async (uid, fieldId, onSuccess=null, onFail=null)=>{
         
        axios.post(
            API_BASE+"fields/unfollow",
            {
                'name': fieldId,
                'uid':uid
            }  
        )
        .catch(onFail)
        .then(res=>{
            onSuccess?.(res.data)
        }) 
    },

    followField: async (uid, fieldId, onSuccess=null, onFail=null)=>{
         
        axios.post(
            API_BASE+"fields/follow",
            {
                'name': fieldId,
                'uid':uid
            }  
        )
        .catch(onFail)
        .then(res=>{
            onSuccess?.(res.data)
        }) 
    },

    getFields: async (query, onSuccess=null, onFail = null)=>{
        //query keys 
        // search: the search string or null if no search string exists
        // sort_by: boolean to sort results. values: "name", "seekers", "opp", or "" for no sort

        // follower_id for followed by

        let data = {"testing": "n"}

        if(query.name) data.search = query.name
        if(query.sort_by) data.sort_by = query.sort_by
        if(query.follower_id) data.follower_id = query.follower_id


        axios.get(
            API_BASE+"fields",
            {
               params: data
            }
        )
        .then(res=>{
            console.log(res)
            onSuccess?.(res.data)
        })
    },

    getField: async (id, onSuccess=null, onFail = null)=>{
        //query keys 
        // id: id of field

        axios.get(
            API_BASE+"fields/field",
            {
              params: {'name': id}
            }
        )
        .then(res=>{
            console.log(res)
            onSuccess?.(res.data)
        })

    },

    addField: async (field, onSuccess=null, onFail=null)=>{

        //field keys: 
        // name: string
        // description: string

        axios.post(
            API_BASE+"fields/field",
            field
        )
        .catch(onFail)
        .then(res=>{
            onSuccess?.(res.data)
        }) 
    },

    editField: async (id, field, onSuccess=null, onFail=null)=>{


        console.log(id, field)
        const data = {
            "id": id,
            "name": field.name,
            "description": field.description
        }

        axios.patch(
            API_BASE+"fields/field",
            data
        )
        .catch(onFail)
        .then(res=>{

            onSuccess?.(res.data)
        }) 
    },

    deleteField: async (id, onSuccess=null, onFail=null)=>{

        axios.delete(
            API_BASE+"fields/field",
            {
                data:{
                    "id":id
                }
            }
        )
        .then(onSuccess)
    },

    getOrganizations: async (query, onSuccess=null, onFail=null)=>{
      
        //query keys:
        // name: string
        // optional location
        // sort_by: name, mentors, opp, comp, or null
        // avg, max, min ,... stats in details
        let data = {}

        if(query.name) data.search = query.name
        if(query.location) data.location = query.location
        if(query.sort_by) data.sort_by = query.sort_by

        

        axios.get(
            API_BASE+"organizations",
            {
              params: data
            }
        )
        .then(res=>{
            console.log(res)
            onSuccess?.(res.data)
        })
    },

    getOrganization: async (id, onSuccess=null, onFail = null)=>{

        axios.get(
            API_BASE+"organizations/"+id
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },

    addOrganization: async (org, onSuccess=null, onFail=null)=>{

        const data = {
            name: org.name,
            email: org.email,
            website: org.website,
            location: org.location,
            is_educational: (org.educational== "true")
        }

        axios.post(
            API_BASE+"organizations/"+org.email,
            data
        )
        .catch(onFail)
        .then(res=>{
            onSuccess?.(res.data)
        }) 
    },

    editOrganization: async (id, org, onSuccess=null, onFail=null)=>{


        const data = {
            id: id,
            name: org.name,
            email: org.email,
            website: org.website,
            location: org.location,
            is_educational: (org.educational== "true")
        }

        axios.patch(
            API_BASE+"organizations/"+id,
            data
        )
        .catch(onFail)
        .then(res=>{
            onSuccess?.(res.data)
        }) 
    },

    deleteOrganization: async (id, onSuccess=null, onFail=null)=>{


        axios.delete(
            API_BASE+"organizations/"+id
        )
        .then(onSuccess)
    },
    

    getPostedOpportunities: async (uid, onSuccess=null, onFail = null)=>{

        onSuccess?.(
            [
                {
                    "id": 10,
                    "name": "Software intern",
                    "org_id": "4",
                    "org_name": "American University of beirut",
                    "location": "Beirut, Lebanon",
                    "deadline_date": "2020-04-21",
                    "poster_id": "293",
                    "poster_email": "mentor@bla.com",
                    "poster_name": "Karim Jamil",
                    "n_seekers": 10,
                    "n_mentors": 20
                }
            ]
        )

    },

    getAssociatedOpportunities: async (uid, onSuccess=null, onFail = null)=>{

        onSuccess?.(
            [
                {
                    "id": 10,
                    "name": "Software intern",
                    "org_id": "4",
                    "org_name": "American University of beirut",
                    "location": "Beirut, Lebanon",
                    "deadline_date": "2020-04-21",
                    "poster_id": "293",
                    "poster_email": "mentor@bla.com",
                    "poster_name": "Karim Bla",
                    "n_seekers": 10,
                    "n_mentors": 20
                }
            ]
        )

    },

    getMatchedSeekerOpportunities: async (uid, onSuccess=null, onFail = null)=>{

        onSuccess?.(
            [
                {
                    "id": 10,
                    "name": "Software intern",
                    "org_id": "4",
                    "org_name": "American University of beirut",
                    "location": "Beirut, Lebanon",
                    "deadline_date": "2020-04-21",
                    "poster_id": "293",
                    "poster_email": "mentor@bla.com",
                    "poster_name": "Nadim",

                    "seeker_id": "29",
                    "seeker_name":"George Eid"
                }
            ]
        )

    },

    getAppliedOpportunities: async (uid, onSuccess=null, onFail = null)=>{

        onSuccess?.(
            [
                {
                    "id": 10,
                    "name": "Software intern",
                    "org_id": "4",
                    "org_name": "American University of beirut",
                    "location": "Beirut, Lebanon",
                    "deadline_date": "2020-04-21",
                    "poster_id": "293",
                    "poster_email": "mentor@bla.com",
                    "poster_name": "Nadim",
                    "n_seekers": 10,
                    "n_mentors": 20
                    
                }
            ]
        )

    },

    getMatchedMentorOpportunities: async (uid, onSuccess=null, onFail = null)=>{

        onSuccess?.(
            [
                {
                    "id": 10,
                    "name": "Software intern",
                    "org_id": "4",
                    "org_name": "American University of beirut",
                    "location": "Beirut, Lebanon",
                    "end_date": "2020-04-21",
                    "poster_id": "293",
                    "poster_email": "mentor@bla.com",
                    "poster_name": "Nadim",

                    "mentor_id": "4",
                    "mentor_name": "Toufic"
                }
            ]
        )

    },

    getOpportunities: async (query, onSuccess=null, onFail=null)=>{

        //query keys
        // uid: id of user
        // name: search value for name
        // org_id: filter only for a given org, or null if no filter
        // field_id: filter only for a given field or null if no filter
        // start_after: filter for offers after this date or null if no filter
        // end_before: filter for offers before this date or null if no filter
        // open: true -> filter for offers where deadline still not past else no filter
        // sort_by: 
        //          - "compensation" sort by descending compensation value
        //          - "seekers" sort by descending seeker number
        //          - "mentors" sort by descending mentor number
        //          - "deadline" sort by deadline 

        // return those that the seeker -if user is seeker- did not apply to

        onSuccess?.(
            [
                {
                    "id": 10,
                    "name": "Software intern",
                    "org_id": "4",
                    "org_name": "American University of beirut",
                    "location": "Beirut, Lebanon",
                    "end_date": "2020-04-21",
                    "poster_id": "293",
                    "poster_email": "mentor@bla.com",
                    "poster_name": "Nadim",
                    "n_seekers": 10,
                    "n_mentors": 20,
                    "start_date":"2020-04-21",
                    "deadline_date": "2021-03-21",
                    "compensation": 2000,
                    "compensation_type":"monthly",
                    "field_name": "Software"
                }
            ]
        )

    },

    applyToOpportunity: async(uid, oppid, onSuccess=null, onFail=null)=>{
    
        const data = {
            'uid': uid,
            'opp_id': oppid
        }

         
        onSuccess?.()
    },

    cancelApplyToOpportunity: async(uid, oppid, onSuccess=null, onFail=null)=>{
    
        const data = {
            'uid': uid,
            'opp_id': oppid
        }

         
        onSuccess?.()
    },

    deleteOpportunity: async(oppid, onSuccess=null, onFail=null)=>{
    
        const data = {
            'opp_id': oppid
        }

         
        onSuccess?.()
    },

    editOpportunity: async(oppid, opp, onSuccess=null, onFail=null)=>{
    
        const data = {
            "id": oppid,
            "name": opp.name,
            "org_id": opp.org_id,
            "location": opp.location,
            "end_date": opp.end_date,
            "start_date":opp.start_date,
            "deadline_date": opp.deadline_date,
            "compensation": opp.compensation,
            "compensation_type":opp.compensation_type,
            "field_id": opp.field_id,
            "application_portal_url": opp.portal,
            "description": opp.description,
            "benifits":[
                "h1",
                "h2"
            ]
        }

         
        onSuccess?.()
    },

    addOpportunity: async(uid, oppid, opp, onSuccess=null, onFail=null)=>{
    
        const data = {
            "id": oppid,
            "name": opp.name,
            "poster_id": uid,
            "org_id": opp.org_id,
            "location": opp.location,
            "end_date": opp.end_date,
            "start_date":opp.start_date,
            "deadline_date": opp.deadline_date,
            "compensation": opp.compensation,
            "compensation_type":opp.compensation_type,
            "field_id": opp.field_id,
            "application_portal_url": opp.portal,
            "description": opp.description,
            "benefits": [
                "ben1",
                "ben3",
            ]
        }

         
        onSuccess?.()
    },

    getOpportunity: async(oppid, onSuccess=null, onFail=null)=>{

        onSuccess?.(
            {
                    "id": 10,
                    "name": "Software intern",
                    "description":"oadinfe iofawnefkio wifb o",
                    "org_id": "2",
                    "org_name": "American University of beirut",
                    "location": "Beirut, Lebanon",
                    "end_date": "2020-04-21",
                    "poster_id": "293",
                    "poster_email": "mentor@bla.com",
                    "poster_name": "Nadim",
                    "n_seekers": 10,
                    "n_mentors": 20,
                    "start_date":"2020-04-21",
                    "deadline_date": "2021-03-21",
                    "compensation": 2000,
                    "portal": "https://www.google.com",
                    "compensation_type":"hourly",
                    "field_id": 1,
                    "field_name": "Software",
                    "benifits":[
                        "h1",
                        "h2"
                    ],
            }
        )
    },

    getOpportunityRelation: async (uid, oppid, onSuccess=null, onFail=null)=>{
        const data = {
            'uid': uid,
            'opp_id': oppid
        }

        onSuccess?.(
            {
                'rel': "no_rel", //associated, matchedMentor, matchedSeeker, applied, no_rel
                'uid': 10, // if matchedMentor then the uid is for mentor, if matchedSeeker then uid is for seeker, else null
            }
        )
    },


    getOpportunityBenefits: async(oppid, onSuccess=null, onFail=null)=>{
    
        const data = {
            "opp_id": oppid,
        }

        onSuccess?.([
            {
                'id': 1,
                'content': "snof ienfwenfodn fo"
            },
            {
                'id': 2,
                'content': "snof ienfwenfodn fo"
            },
        ])
    },

    addOpportunityBenefit: async(oppid, benefit, onSuccess=null, onFail=null)=>{
    
        const data = {
            "opp_id": oppid,
            "content": benefit
        }

         
        onSuccess?.()
    },

    editOpportunityBenefit: async(oppid, benefit_id, benefit, onSuccess=null, onFail=null)=>{
    
        const data = {
            "opp_id": oppid,
            "id": benefit_id,
            "content": benefit
        }

         
        onSuccess?.()
    },

    deleteOpportunityBenefit: async(oppid, benefit_id, onSuccess=null, onFail=null)=>{
    
        const data = {
            "opp_id": oppid,
            "id": benefit_id,
        }

         
        onSuccess?.()
    },

    associateOpportunity: async(uid,oppid, onSuccess=null, onFail=null)=>{
    
        const data = {
            "uid": uid,
            "opp_id": oppid,
        }

         
        onSuccess?.()
    },

    dessociateOpportunity: async(uid,oppid, onSuccess=null, onFail=null)=>{
    
        const data = {
            "uid": uid,
            "opp_id": oppid,
        }

         
        onSuccess?.()
    },

    unmatchMentoring: async(mentor_id, seeker_id, opp_id, onSuccess=null, onFail=null)=>{
    
        const data = {
            "uid": mentor_id,
            "seeker_id": seeker_id,
            "opp_id": opp_id,
        }

         
        onSuccess?.()
    },

    matchMentoring: async(mentor_id, seeker_id, opp_id, onSuccess=null, onFail=null)=>{
    
        const data = {
            "mentor_id": mentor_id,
            "seeker_id": seeker_id,
            "opp_id": opp_id,
            "status": "ongoing"
        }

         
        onSuccess?.()
    },

    finishMentoring: async(mentor_id, seeker_id, opp_id, rating, onSuccess=null, onFail=null)=>{
    
        const data = {
            "mentor_id": mentor_id,
            "seeker_id": seeker_id,
            "opp_id": opp_id,
            "status": "finished",
            "rating": rating
        }

         
        onSuccess?.()
    },

    sendMessage: async(uid, other_id, message, onSuccess=null, onFail=null)=>{
    

        // backend must add the current date to the attributes

        const data = {
            "uid": uid,
            "other_id": other_id,
            "message": message,
        }

         
        onSuccess?.()
    },

    getMessage: async(sender_id, receiver_id, onSuccess=null, onFail=null)=>{

        const data = {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
        }

         
        onSuccess?.([
            {
                type: "received",
                message:"Hi ",
                datetime: "2020-03-10 14:00"
            },
            {
                type: "sent",
                message:"By ",
                datetime: "2020-03-10 14:00"
            }
        ])
    },

    getUsers: async(query, onSuccess=null, onFail=null)=>{
    
        // query params
        //  name: search string

        onSuccess?.([
            {
                "name": "Saiid El Hajj Chehade",
                "id": 10
            },
        ])
    },

    getMentors: async(oppid, onSuccess=null, onFail=null)=>{

        onSuccess?.([
            {
                "name": "Saiid El Hajj Chehade",
                "id": 10
            },
        ])
    },
    

    getSeekers: async(oppid, query={}, onSuccess=null, onFail=null)=>{

        //query parameters

        const data = {
            "opp_id": 29, // can be null then return all seekers
            "mentor_id": query.mentor_id, // can be null 
            "pending": query.pending, // boolean: if pending true -> get all applicants not mentored by anyone else return every applicant
        }

        onSuccess?.([
            {
                "name": "Saiid El Hajj Chehade",
                "id": 10
            },
        ])
    },

    getMentoringMentors: async(uid, oppid=null, onSuccess=null, onFail=null)=>{

        const data ={
            uid: uid,
            opp_id: oppid //can be null then return all mentors of uid
        }

        onSuccess?.([
            {
                "name": "Saiid El Hajj Chehade",
                "id": 10
            },
        ])
    },

    getMentoredSeekers: async(uid, oppid=null, onSuccess=null, onFail=null)=>{

        const data ={
            uid: uid,
            opp_id: oppid //can be null then return all mentorees of uid
        }

        onSuccess?.([
            {
                "name": "Saiid El Hajj Chehade",
                "id": 10
            },
        ])
    },




}