// Global store utils
export const onlyUnique = function(value, index, self) {
  return self.indexOf(value) === index;
}

export const obj2slug = function(obj) {
  let id = obj.id
  let value = obj.name

  let slug = id+'-'+value.toString()
    .substring(0,40)
    .replace(/\s/g, "-")
    .toLowerCase()
  return encodeURI(slug)
}

export const slug2id = function(slug) {
  return parseInt(slug.split('-')[0])
}