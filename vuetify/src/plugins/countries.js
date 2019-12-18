import { Countries } from "@/plugins/i18n";

export function demonym(iso3) {
  return Countries.filter(c => c.alpha3Code == iso3)[0].demonym;
}

export function iso3toiso2(iso3) {
  return Countries.filter(c => c.alpha3Code == iso3)[0].alpha2Code;
}

export function translateCountryName(iso3, locale) {
  let countryData = Countries.filter(c => c.alpha3Code == iso3)[0];
  return countryData.translations[locale] || countryData.name;
}
