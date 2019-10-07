// Global store utils
export const onlyUnique = function(value, index, self) {
  return self.indexOf(value) === index;
};

export const obj2slug = function(obj, nameAttr = "name") {
  let id = obj.id;
  let value = obj[nameAttr];

  if (!value) {
    return id;
  }

  let slug =
    id +
    "-" +
    value
      .toString()
      .substring(0, 40)
      .replace(/\s/g, "-")
      .toLowerCase();
  return encodeURI(slug);
};

export const slug2id = function(slug) {
  return parseInt(slug.split("-")[0]);
};

// Async Download

export const donwloadAsyncCSV = async function($vm, url, filename) {
  let data = (await $vm.$http.get(url)).bodyText;

  var file = new Blob([data], { type: "text/plain" });

  if (window.navigator.msSaveOrOpenBlob)
    // IE10+
    window.navigator.msSaveOrOpenBlob(file, filename);
  else {
    // Others
    var a = document.createElement("a");
    var url = URL.createObjectURL(file);
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(function() {
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    }, 0);
  }
};

// ==================================
//  REGEX TESTERS
// ==================================

const REGEX_URL = new RegExp(/^https?:\/\/[^\s/$.?#].[^\s]*$/i);
const REGEX_EMAIL = new RegExp(
  /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
);

export const regexIsURL = function(value) {
  if (!value || value == "") return true;
  return REGEX_URL.test(value);
};

export const regexIsEmail = function(value) {
  if (!value || value == "") return true;
  return REGEX_EMAIL.test(String(value).toLowerCase());
};
