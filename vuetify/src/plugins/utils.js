// Global store utils
export const onlyUnique = function(value, index, self) {
  return self.indexOf(value) === index;
}

export const obj2slug = function(obj, nameAttr="name") {
  let id = obj.id
  let value = obj[nameAttr]

  if (!value){
    return id
  }

  let slug = id+'-'+value.toString()
    .substring(0,40)
    .replace(/\s/g, "-")
    .toLowerCase()
  return encodeURI(slug)
}

export const slug2id = function(slug) {
  return parseInt(slug.split('-')[0])
}


// ==================================
//  REGEX TESTERS
// ==================================

const REGEX_URL = new RegExp(/^https?:\/\/[^\s/$.?#].[^\s]*$/i)

export const regexIsURL = function(value){
  if(value == '') return true;
  return REGEX_URL.test(value)
}