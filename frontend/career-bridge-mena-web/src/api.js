export default {

    getUser: async (uid, onSuccess=null, onFail=null) => {
        onSuccess?.({
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
    }

}