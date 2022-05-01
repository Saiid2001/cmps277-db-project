export default {

    getUser: async (uid, onSuccess=null, onFail=null) => {
        onSuccess?.({
            uid: uid,
            first_name: "Saiid",
            last_name: "El Hajj Chehade",
            birth_date: "2001-06-22",
            linkedin: "/linkedin/saiidhajjchehade",
            website: "www.saiid.com",
            phone: "78818109"
        })
    },

    USER_TYPES: {
        "Mentor": "M",
        "Seeker": "S"
    }

    ,getUserType: async (uid, onSuccess=null, onFail=null) =>{
        onSuccess?.(
            "M"
        )
    },

    setUser: async (uid, info, onSuccess = null, onFail = null)=>{
        info.uid=uid
        console.log(info)
            
        // first_name, last_name, birth_date, linkedin, website, phone, gender
    },

    getCurrentPosition: async(uid, onSuccess = null, onFail = null)=>{

        console.log("h")
        onSuccess?.(
            {
                "position": "Analysit",
                "org_name": "BCG",
                "org_id": "1"
            }
        )

    },

    setCurrentPosition: async(uid, info, onSuccess = null, onFail = null)=>{
        console.log(info)
        
        //position org_id
    },

    getAllOrganizationNames: async( onSuccess = null, onFail = null)=>{
        onSuccess?.(
            [
                {"org_name": "BCG" , "org_id": "1"},
                {"org_name": "ABC" , "org_id": "2"},
                {"org_name": "Total" , "org_id": "3"},
            ]
        )
    }, 

    getSeekerData: async (uid, onSuccess=null, onFail=null)=>{

        onSuccess?.(
            {
                'sop': "this is statement of purose",
                'open_to_work': true
            }
        )
    },

    setSeekerData: async (uid, info, onSuccess=null, onFail=null)=>{

        console.log(info)
        
        // sop, open_to_work

    },

    getEducations: async (uid, onSuccess=null, onFail=null)=>{

        onSuccess?.(
            [
                {
                    "major": "Computer Communication Engineering",
                    "org_id": "1",
                    "org_name": "American University of Beirut",
                    "score": "4.0 GPA",
                    "accomplishments":[
                        "a1","a2"
                    ],
                    "start_at": "2020-03-21",
                    "end_at": "2020-03-21"
                },
                {
                    "major": "Computer Communication Engineering",
                    "org_id": "1",
                    "org_name": "American University of Beirut",
                    "score": "4.0 GPA",
                    "accomplishments":[
                        "a1","a2"
                    ],
                    "start_at": "2020-03-21",
                    "end_at": "2020-04-21"
                },
            ]
        )

    },

    deleteEducation: async (uid, program, onSuccess=null, onFail=null)=>{
        console.log(program)
        
        //program id
    },

    setEducation: async (uid, program, onSuccess=null, onFail=null)=>{
        console.log(program)
    },
    

    getExperiences: async (uid, onSuccess=null, onFail=null)=>{
        onSuccess?.(
            [
               {
                   "position": "Analyst",
                   "org_id": "2",
                   "org_name":"Analytica",
                   "start_at": "2020-03-03",
                   "end_at": "2021-03-04",
                   "accomplishments":["a", "b", "c"]
               } 
            ]
        )
    },

    setExperience: async (uid, experience, onSuccess=null, onFail=null)=>{
        console.log(experience)
    },
    deleteExperience: async (uid, experience, onSuccess=null, onFail=null)=>{
        console.log(experience)
    },

    getProjects: async (uid, onSuccess=null, onFail=null)=>{
        onSuccess?.(
            [
                {
                    "name": "this is a project bla",
                    "description": "djfiokenfen fewof edf aj fedna fr ke fedn afek kd fa ewjk dfaK QERFAEF",
                    "date":"2020-03-03"
                }
            ]
        )
    },

    setProject: async (uid, project, onSuccess=null, onFail=null)=>{
        console.log(project)
    },
    deleteProject: async (uid, project, onSuccess=null, onFail=null)=>{
        console.log(project)
    },
    getCertifications: async (uid, onSuccess=null, onFail=null)=>{
        onSuccess?.(
            [
                {
                    "name": "this is a project bla",
                    "url": "https://www.google.com",
                    "date":"2020-03-03"
                }
            ]
        )
    },

    setCertification: async (uid, project, onSuccess=null, onFail=null)=>{
        console.log(project)
    },
    deleteCertification : async (uid, project, onSuccess=null, onFail=null)=>{
        console.log(project)
    },

    getSkills: async (uid, onSuccess=null, onFail=null)=>{
        onSuccess?.(
            [
                "skill 1",
                "skill 2"
            ]
        )
    },

    setSkills: async (uid, skills, onSuccess=null, onFail=null)=>{
        console.log(skills)
    },
    
    getFollowedFields: async (uid, onSuccess=null, onFail = null)=>{
        onSuccess?.(
            [
                    {
                        id: "2",
                        name: "Field 1",
                        n_seekers: 100,
                        n_opportunities: 200,
                    },
                    {
                        id: "3",
                        name: "Field 2",
                        n_seekers: 100,
                        n_opportunities: 200,
                    },
                    {
                        id: "4",
                        name: "Field 3",
                        n_seekers: 100,
                        n_opportunities: 200,
                    },
                    {
                        id: "5",
                        name: "Field 4",
                        n_seekers: 100,
                        n_opportunities: 200,
                    }
                    ,
                    {
                        id: "6",
                        name: "Field 4",
                        n_seekers: 100,
                        n_opportunities: 200,
                    }
                    ,
                    {
                        id: "7",
                        name: "Field 4",
                        n_seekers: 100,
                        n_opportunities: 200,
                    }
                    ,
                    {
                        id: "8",
                        name: "Field 4",
                        n_seekers: 100,
                        n_opportunities: 200,
                    }
                    ,
                    {
                        id: "9",
                        name: "Field 4",
                        n_seekers: 100,
                        n_opportunities: 200,
                    }
                ]

            
        )
    },

    unfollowField: async (uid, fieldId, onSuccess=null, onFail=null)=>{
        console.log("unfollowed "+fieldId);
        onSuccess?.()
    },

    followField: async (uid, fieldId, onSuccess=null, onFail=null)=>{
        console.log("followed "+fieldId);
        onSuccess?.()
    },

    getFields: async (query, onSuccess=null, onFail = null)=>{
        //query keys 
        // name: the search string or null if no search string exists
        // sort_by: boolean to sort results. values: "name", "seekers", "opp", or "" for no sort

        onSuccess?.([
            {
                "id": 1,
                "name": "Software",
                "description": "djfiokenfen fewof edf aj fedna fr ke fedn afek kd fa ewjk dfaK QERFAEF",
                "n_seekers": 10,
                "n_opportunities": 100,
            },
            {
                "id": 2,
                "name": "Hardware",
                "description": "djfiokenfen fewof edf aj fedna fr ke fedn afek kd fa ewjk dfaK QERFAEF",
                "n_seekers": 100,
                "n_opportunities": 10,
            }
        ])
    },

    getField: async (id, onSuccess=null, onFail = null)=>{
        //query keys 
        // id: id of field

        onSuccess?.(
            {
                "id": 1,
                "name": "this is a field bla",
                "description": "djfiokenfen fewof edf aj fedna fr ke fedn afek kd fa ewjk dfaK QERFAEF",
               
            }
            )
    },

    addField: async (field, onSuccess=null, onFail=null)=>{

        //field keys: 
        // name: string
        // description: string

        console.log(field);
        onSuccess?.();
    },

    editField: async (id, field, onSuccess=null, onFail=null)=>{


        const data = {
            "id": id,
            "name": field.name,
            "description": field.description
        }



        console.log(data);
        onSuccess?.();
    },

    deleteField: async (id, onSuccess=null, onFail=null)=>{


        const data = {
            "id": id,
        }

        console.log(data);
        onSuccess?.();
    },

    getOrganizations: async (query, onSuccess=null, onFail=null)=>{
      
        //query keys:
        // name: string
        // sort_by: name, mentors, opp, or null

        // avg, max, min ,... stats in details


        onSuccess?.([
            {
                "id": "4",
                "name": "American University of Beirut",
                "location":"Beirut",
                "n_mentors": 100,
                "n_opportunities": 10
            },

            {
                "id": "5",
                "name": "Microsoft",
                "location":"US",
                "n_mentors": 100,
                "n_opportunities": 10
            },

            {
                "id": "6",
                "name": "Google",
                "location":"US",
                "n_mentors": 100,
                "n_opportunities": 10
            },
        ]);
    },

    getOrganization: async (id, onSuccess=null, onFail = null)=>{

        onSuccess?.(
            {
                "id": 1,
                "name": "American University of Beirut",
                "email": "info@aub.edu.lb",
                "website":"https://aub.edu.lb",
                "location":"Beirut, Lebanon",
                "is_educational": true,
                "n_mentors": 20,
                "n_opportunities": 100,
                "max_compensation": 1000,
                "min_compensation": 300,
                "avg_compensation": 500,
            }
            )
    },

    addOrganization: async (org, onSuccess=null, onFail=null)=>{

        const data = {
            name: org.name,
            email: org.email,
            website: org.website,
            location: org.location,
            is_educational: (org.educational== "true")
        }

        console.log(data);
        onSuccess?.();
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

        console.log(data);
        //onSuccess?.();
    },

    deleteField: async (id, onSuccess=null, onFail=null)=>{


        const data = {
            "id": id,
        }

        console.log(data);
        onSuccess?.();
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

        console.log(data)
        onSuccess?.()
    },

    cancelApplyToOpportunity: async(uid, oppid, onSuccess=null, onFail=null)=>{
    
        const data = {
            'uid': uid,
            'opp_id': oppid
        }

        console.log(data)
        onSuccess?.()
    },

    deleteOpportunity: async(oppid, onSuccess=null, onFail=null)=>{
    
        const data = {
            'opp_id': oppid
        }

        console.log(data)
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

        console.log(data)
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

        console.log(data)
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

        console.log(data)
        onSuccess?.()
    },

    editOpportunityBenefit: async(oppid, benefit_id, benefit, onSuccess=null, onFail=null)=>{
    
        const data = {
            "opp_id": oppid,
            "id": benefit_id,
            "content": benefit
        }

        console.log(data)
        onSuccess?.()
    },

    deleteOpportunityBenefit: async(oppid, benefit_id, onSuccess=null, onFail=null)=>{
    
        const data = {
            "opp_id": oppid,
            "id": benefit_id,
        }

        console.log(data)
        onSuccess?.()
    },

    associateOpportunity: async(uid,oppid, onSuccess=null, onFail=null)=>{
    
        const data = {
            "uid": uid,
            "opp_id": oppid,
        }

        console.log(data)
        onSuccess?.()
    },

    dessociateOpportunity: async(uid,oppid, onSuccess=null, onFail=null)=>{
    
        const data = {
            "uid": uid,
            "opp_id": oppid,
        }

        console.log(data)
        onSuccess?.()
    },

    unmatchMentoring: async(mentor_id, seeker_id, opp_id, onSuccess=null, onFail=null)=>{
    
        const data = {
            "uid": mentor_id,
            "seeker_id": seeker_id,
            "opp_id": opp_id,
        }

        console.log(data)
        onSuccess?.()
    },

    matchMentoring: async(mentor_id, seeker_id, opp_id, onSuccess=null, onFail=null)=>{
    
        const data = {
            "mentor_id": mentor_id,
            "seeker_id": seeker_id,
            "opp_id": opp_id,
            "status": "ongoing"
        }

        console.log(data)
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

        console.log(data)
        onSuccess?.()
    },

    sendMessage: async(uid, other_id, message, onSuccess=null, onFail=null)=>{
    

        // backend must add the current date to the attributes

        const data = {
            "uid": uid,
            "other_id": other_id,
            "message": message,
        }

        console.log(data)
        onSuccess?.()
    },

    getMessage: async(sender_id, receiver_id, onSuccess=null, onFail=null)=>{

        const data = {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
        }

        console.log(data)
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