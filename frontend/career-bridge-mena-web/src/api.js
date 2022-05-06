import axios from 'axios';

import { ReactSession } from 'react-client-session';

import config from "./config.json";

const API_BASE = config.API_BASE;

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
            alert("Failed to login")
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
            console.error(res)
            alert("Failed to signup")
            onFail?.()
        })
        .then(res=>{

            console.log(res)
             

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
        ).catch(()=>{
            alert("Cannot delete education")
        })
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
        ).catch(()=>{
            alert("Cannot delete experience")
        })
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
        ).catch(()=>{
            alert("Cannot delete project")
        })
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
        .catch(()=>{
            alert("Cannot delete field")
        })
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
        .catch(()=>{
            alert("Cannot delete organization")
        })
    },
    

    getPostedOpportunities: async (uid, onSuccess=null, onFail = null)=>{

        axios.get(
            API_BASE+"opportunities/posted/"+uid
        )
        .then(res=>{
            onSuccess(res.data)
        })

    },

    getAssociatedOpportunities: async (uid, onSuccess=null, onFail = null)=>{

        axios.get(
            API_BASE+"opportunities/associated/"+uid
        )
        .then(res=>{
            onSuccess(res.data)
        })

    },

    getMatchedSeekerOpportunities: async (uid, onSuccess=null, onFail = null)=>{

        axios.get(
            API_BASE+"opportunities/matchedSeeker/"+uid
        )
        .then(res=>{
            onSuccess(res.data)
        })

    },

    getAppliedOpportunities: async (uid, onSuccess=null, onFail = null)=>{

        axios.get(
            API_BASE+"opportunities/applied/"+uid
        )
        .then(res=>{
            onSuccess(res.data)
        })

    },

    getMatchedMentorOpportunities: async (uid, onSuccess=null, onFail = null)=>{

        axios.get(
            API_BASE+"opportunities/matchedMentor/"+uid
        )
        .then(res=>{
            onSuccess(res.data)
        })

    },

    getOpportunities: async (uid, query, onSuccess=null, onFail=null)=>{

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
        //not_applied: user id of student not applying to following opps

        // return those that the seeker -if user is seeker- did not apply to

        let data = {}

        for(var key in query){
            if(query[key]) data[key] = query[key]
        }

        if(data.name){
            data.search = data.name;
            delete data.name
        }

        axios.get(
            API_BASE+"opportunities",
            {
                params:data
            }
        )
        .then(res=>{
            console.log(res.data)
            onSuccess(res.data)
        })

    },

    applyToOpportunity: async(uid, oppid, onSuccess=null, onFail=null)=>{
    

        console.log(uid, oppid)
        const data = {
            'uid': uid,
            'opp_id': oppid
        }

         
        axios.post(
            API_BASE+"opportunities/"+uid+"/apply/"+oppid
        )
        .then(onSuccess)
    },

    cancelApplyToOpportunity: async(uid, oppid, onSuccess=null, onFail=null)=>{
    
        const data = {
            'uid': uid,
            'opp_id': oppid
        }

         
        axios.delete(
            API_BASE+"opportunities/"+uid+"/cancel/"+oppid
        )
        .then(onSuccess)
    },

    deleteOpportunity: async(oppid, onSuccess=null, onFail=null)=>{
    
        const data = {
            'opp_id': oppid
        }

        axios.delete(
            API_BASE+"opportunities/"+oppid
        )
        .then(onSuccess)
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
            "benefits":opp.benefits
        }

         
        axios.patch(
            API_BASE+"opportunities/"+oppid,
            data
        )
        .then(onSuccess)
    },

    addOpportunity: async(uid, opp, onSuccess=null, onFail=null)=>{
    
        const data = {
            "id": opp.id,
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
            "benefits": opp.benefits
        }

         
        axios.post(
            API_BASE+"opportunities/0",
            data
        )
        .then(onSuccess)
    },

    getOpportunity: async(oppid, onSuccess=null, onFail=null)=>{

        axios.get(
            API_BASE+"opportunities/"+oppid
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },

    getOpportunityRelation: async (uid, oppid, onSuccess=null, onFail=null)=>{
        const data = {
            'uid': uid,
            'opp_id': oppid
        }

        axios.get(
            API_BASE+"opportunities/"+uid+"/rel/"+oppid
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },


    getOpportunityBenefits: async(oppid, onSuccess=null, onFail=null)=>{
    
        const data = {
            "opp_id": oppid,
        }

        axios.get(
            API_BASE+"opportunities/"+oppid+"/benefits"
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },

    addOpportunityBenefit: async(oppid, benefit, onSuccess=null, onFail=null)=>{
    
        const data = {
            "opp_id": oppid,
            "content": benefit
        }

         
        axios.post(
            API_BASE+"opportunities/"+oppid+"/benefits",
            data
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },

    editOpportunityBenefit: async(oppid, benefit_id, benefit, onSuccess=null, onFail=null)=>{
    
        const data = {
            "opp_id": oppid,
            "id": benefit_id,
            "content": benefit
        }

         
        axios.patch(
            API_BASE+"opportunities/"+oppid+"/benefits",
            data
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },

    deleteOpportunityBenefit: async(oppid, benefit_id, onSuccess=null, onFail=null)=>{
    
        const data = {
            "opp_id": oppid,
            "id": benefit_id,
        }

         
        axios.post(
            API_BASE+"opportunities/"+oppid+"/benefits/delete",
            data
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },

    associateOpportunity: async(uid,oppid, onSuccess=null, onFail=null)=>{
    
        const data = {
            "uid": uid,
            "opp_id": oppid,
        }

         
        axios.post(
            API_BASE+"opportunities/"+uid+"/associate/"+oppid
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },

    dessociateOpportunity: async(uid,oppid, onSuccess=null, onFail=null)=>{
    
        const data = {
            "uid": uid,
            "opp_id": oppid,
        }

         
        axios.delete(
            API_BASE+"opportunities/"+uid+"/associate/"+oppid
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },

    unmatchMentoring: async(mentor_id, seeker_id, opp_id, onSuccess=null, onFail=null)=>{
    
        const data = {
            "uid": mentor_id,
            "seeker_id": seeker_id,
            "opp_id": opp_id,
        }

         
        axios.post(
            API_BASE+"opportunities/"+opp_id+"/"+mentor_id+"/cancelMentoring/"+seeker_id
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },

    matchMentoring: async(mentor_id, seeker_id, opp_id, onSuccess=null, onFail=null)=>{
    
        const data = {
            "mentor_id": mentor_id,
            "seeker_id": seeker_id,
            "opp_id": opp_id,
            "status": "ongoing"
        }

         
        axios.post(
            API_BASE+"opportunities/"+opp_id+"/"+mentor_id+"/mentor/"+seeker_id
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },

    finishMentoring: async(mentor_id, seeker_id, opp_id, rating, onSuccess=null, onFail=null)=>{
    
        const data = {
            "mentor_id": mentor_id,
            "seeker_id": seeker_id,
            "opp_id": opp_id,
            "status": "finished",
            "rating": rating
        }

         
        axios.post(
            API_BASE+"opportunities/"+opp_id+"/"+mentor_id+"/finishMentoring/"+seeker_id,
            data
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },

    sendMessage: async(uid, other_id, message, onSuccess=null, onFail=null)=>{
    

        // backend must add the current date to the attributes

        const data = {
            "uid": uid,
            "other_id": other_id,
            "message": message,
        }

         
        axios.post(
            API_BASE+"messages/"+uid+"/message/"+other_id,
            data
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },

    getMessage: async(sender_id, receiver_id, onSuccess=null, onFail=null)=>{

        const data = {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
        }

         
        axios.get(
            API_BASE+"messages/"+sender_id+"/message/"+receiver_id,
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },

    getUsers: async(query, onSuccess=null, onFail=null)=>{
    
        // query params
        //  name: search string
        // type

        let data = {}

        for(var key in query){
            if(query[key]) data[key] = query[key]
        }

        if(data.name){
            data.search = data.name;
            delete data.name
        }


        axios.get(
            API_BASE+"users",
            {
                params: data
            }
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },

    getMentors: async(oppid, onSuccess=null, onFail=null)=>{

        axios.get(
            API_BASE+"mentors/"+oppid
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },
    

    getSeekers: async(oppid, query={}, onSuccess=null, onFail=null)=>{

        //query parameters

        const data = {
            "mentor_id": query.mentor_id, // can be null 
            "pending": query.pending, // boolean: if pending true -> get all applicants not mentored by anyone else return every applicant
        }

        axios.get(
            API_BASE+"seekers/"+oppid,
            {
                params: data
            }
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },

    getMentoringMentors: async(uid, oppid=null, onSuccess=null, onFail=null)=>{

        const data ={
            uid: uid,
            opp_id: oppid //can be null then return all mentors of uid
        }

        console.log(data)

        axios.get(
            API_BASE+"mentoringMentors/"+uid,
            {params: data}
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },

    getMentoredSeekers: async(uid, oppid=null, onSuccess=null, onFail=null)=>{

        const data ={
            uid: uid,
            opp_id: oppid //can be null then return all mentorees of uid
        }

        axios.get(
            API_BASE+"mentoredSeekers/"+uid,
            {params: data}
        )
        .then(res=>{
            onSuccess(res.data)
        })
    },




}