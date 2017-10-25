function submitMyform () {
/***********Traitement double saisie**************/
/****************************************************************/
// 
// saisie: /var/www/localhost/htdocs/test/online/js/submit_script
// c = online_controle
// l = online_rejet
var form = document.forms.frm_saisie;
for (i=0 ; i<= form.length-1 ; i++)
{
if (form[i].type == 'text' && form[i].name.substr(form[i].name.length-3,3)=='_d2')
{
	if ($("#"+form[i].name.substr(0,form[i].name.length-3)).val()!=$("#" + form[i].name).val())
	{
		$("#" + form[i].name.substr(0,form[i].name.length-3)).val("");
		$("#" + form[i].name).val("");
		alert("Champs double saisie " + form[i].name.substr(0,form[i].name.length-3) + " et " + form[i].name + " differents");
		$("#" + form[i].name.substr(0,form[i].name.length-3)).focus();
		return false;
	}
}
}
/****************************************************************/
/***********Fin traitement double saisie**************/
/*alert("aaaaaa")*/
var est_ce_un_professionnel                     = $('#est_ce_un_professionnel').val();
var siren                     = $('#siren').val();
var iban                     = $('#iban').val();
var bic                     = $('#bic').val();
var presence_facture_ou_tc                     = $('#presence_facture_ou_tc').val();
var presence_achat_mobile                     = $('#presence_achat_mobile').val();
var date_sur_facture                     = $('#date_sur_facture').val();
var montant_ttc_mobile                     = $('#montant_ttc_mobile').val();
var montant_ht_mobile                     = $('#montant_ht_mobile').val();
var presence_code_barre_mobile                     = $('#presence_code_barre_mobile').val();
var saisie_code_barre_mobile                     = $('#saisie_code_barre_mobile').val();
var presence_imei                     = $('#presence_imei').val();
var saisie_imei                     = $('#saisie_imei').val();
var presence_bulletin                     = $('#presence_bulletin').val();
var j_accepte_de_recevoir                     = $('#j_accepte_de_recevoir').val();
var msg = '';

/***********  UTILISATION FONCTION VALIDE  CAS POSSIBLE **************/

var valide1 = valider_1(est_ce_un_professionnel,siren);
if(!valide1) {
	msg += '1 - Vérifier l\'interdépendance des champs: est_ce_un_professionnel / siren \n';
	$('#est_ce_un_professionnel').css('border', '1px solid red');
	$('#siren').css('border', '1px solid red');
}
else {
	$('#est_ce_un_professionnel').css('border', '1px inset #ececec');
	$('#siren').css('border', '1px inset #ececec');
}

/****************************************************************/
/****************************************************************/
/****************************************************************/

var valide2 = valider_2(iban,bic);
if(!valide2) {
	msg += '2 - Vérifier l\'interdépendance des champs: iban / bic \n';
	$('#iban').css('border', '1px solid red');
	$('#bic').css('border', '1px solid red');
}
else {
	$('#iban').css('border', '1px inset #ececec');
	$('#bic').css('border', '1px inset #ececec');
}

/****************************************************************/
/****************************************************************/
/****************************************************************/

var valide3 = valider_3(presence_facture_ou_tc,presence_achat_mobile,date_sur_facture);
if(!valide3) {
	msg += '3 - Vérifier l\'interdépendance des champs: presence_facture_ou_tc / presence_achat_mobile / date_sur_facture \n';
	$('#presence_facture_ou_tc').css('border', '1px solid red');
	$('#presence_achat_mobile').css('border', '1px solid red');
	$('#date_sur_facture').css('border', '1px solid red');
}
else {
	$('#presence_facture_ou_tc').css('border', '1px inset #ececec');
	$('#presence_achat_mobile').css('border', '1px inset #ececec');
	$('#date_sur_facture').css('border', '1px inset #ececec');
}

/****************************************************************/
/****************************************************************/
/****************************************************************/

var valide4 = valider_4(presence_achat_mobile,montant_ttc_mobile,montant_ht_mobile);
if(!valide4) {
	msg += '4 - Vérifier l\'interdépendance des champs: presence_achat_mobile / montant_ttc_mobile / montant_ht_mobile \n';
	$('#presence_achat_mobile').css('border', '1px solid red');
	$('#montant_ttc_mobile').css('border', '1px solid red');
	$('#montant_ht_mobile').css('border', '1px solid red');
}
else {
	$('#presence_achat_mobile').css('border', '1px inset #ececec');
	$('#montant_ttc_mobile').css('border', '1px inset #ececec');
	$('#montant_ht_mobile').css('border', '1px inset #ececec');
}

/****************************************************************/
/****************************************************************/
/****************************************************************/

var valide5 = valider_5(presence_code_barre_mobile,saisie_code_barre_mobile);
if(!valide5) {
	msg += '5 - Vérifier l\'interdépendance des champs: presence_code_barre_mobile / saisie_code_barre_mobile \n';
	$('#presence_code_barre_mobile').css('border', '1px solid red');
	$('#saisie_code_barre_mobile').css('border', '1px solid red');
}
else {
	$('#presence_code_barre_mobile').css('border', '1px inset #ececec');
	$('#saisie_code_barre_mobile').css('border', '1px inset #ececec');
}

/****************************************************************/
/****************************************************************/
/****************************************************************/

var valide6 = valider_6(presence_imei,saisie_imei);
if(!valide6) {
	msg += '6 - Vérifier l\'interdépendance des champs: presence_imei / saisie_imei \n';
	$('#presence_imei').css('border', '1px solid red');
	$('#saisie_imei').css('border', '1px solid red');
}
else {
	$('#presence_imei').css('border', '1px inset #ececec');
	$('#saisie_imei').css('border', '1px inset #ececec');
}

/****************************************************************/
/****************************************************************/
/****************************************************************/

var valide7 = valider_7(presence_bulletin,j_accepte_de_recevoir);
if(!valide7) {
	msg += '7 - Vérifier l\'interdépendance des champs: presence_bulletin / j_accepte_de_recevoir \n';
	$('#presence_bulletin').css('border', '1px solid red');
	$('#j_accepte_de_recevoir').css('border', '1px solid red');
}
else {
	$('#presence_bulletin').css('border', '1px inset #ececec');
	$('#j_accepte_de_recevoir').css('border', '1px inset #ececec');
}

/****************************************************************/

if(msg=='')
	{
		$.ajax({
			url: 'save_frm_data.php',
			type: 'POST',
			data: $('#frm_saisie').serialize(),
			success: function(result) {
				all_requete(result);
				},
			async: false
		});
	}
else
	{
		alert(msg);
		if(!valide1){
			$('#est_ce_un_professionnel').focus();
			return false;
		}
		if(!valide2){
			$('#iban').focus();
			return false;
		}
		if(!valide3){
			$('#presence_facture_ou_tc').focus();
			return false;
		}
		if(!valide4){
			$('#presence_achat_mobile').focus();
			return false;
		}
		if(!valide5){
			$('#presence_code_barre_mobile').focus();
			return false;
		}
		if(!valide6){
			$('#presence_imei').focus();
			return false;
		}
		if(!valide7){
			$('#presence_bulletin').focus();
			return false;
		}
		return false;
	}
};

/***********  DECLARATION FONCTION VALIDE  CAS POSSIBLE **************/

function valider_1(est_ce_un_professionnel,siren) {
	ret = false;
	v1 = "0";
	v2 = "";


	if (est_ce_un_professionnel!="")    {v1 = est_ce_un_professionnel;}
	if (siren!="")    {v2 = siren;}

	/* test des informations */
	if ((v1=="1") && (v2!="")) {ret = true;}
	if ((v1=="0") && (v2=="")) {ret = true;}
	if ((v1=="1") && (v2=="")) {ret = true;}

	return ret;
}


function valider_2(iban,bic) {
	ret = false;
	v1 = "";
	v2 = "";


	if (iban!="")    {v1 = iban;}
	if (bic!="")    {v2 = bic;}

	/* test des informations */
	if ((v1!="") && (v2!="")) {ret = true;}
	if ((v1=="") && (v2=="")) {ret = true;}

	return ret;
}


function valider_3(presence_facture_ou_tc,presence_achat_mobile,date_sur_facture) {
	ret = false;
	v1 = "0";
	v2 = "0";
	v3 = "";


	if (presence_facture_ou_tc!="")    {v1 = presence_facture_ou_tc;}
	if (presence_achat_mobile!="")    {v2 = presence_achat_mobile;}
	if (date_sur_facture!="")    {v3 = date_sur_facture;}

	/* test des informations */
	if ((v1=="1") && (v2=="1") && (v3!="")) {ret = true;}
	if ((v1=="1") && (v2=="1") && (v3=="")) {ret = true;}
	if ((v1=="1") && (v2=="0") && (v3=="")) {ret = true;}
	if ((v1=="1") && (v2=="0") && (v3!="")) {ret = true;}
	if ((v1=="0") && (v2=="0") && (v3=="")) {ret = true;}

	return ret;
}


function valider_4(presence_achat_mobile,montant_ttc_mobile,montant_ht_mobile) {
	ret = false;
	v1 = "0";
	v2 = "";
	v3 = "";


	if (presence_achat_mobile!="")    {v1 = presence_achat_mobile;}
	if (montant_ttc_mobile!="")    {v2 = montant_ttc_mobile;}
	if (montant_ht_mobile!="")    {v3 = montant_ht_mobile;}

	/* test des informations */
	if ((v1=="1") && (v2!="") && (v3=="")) {ret = true;}
	if ((v1=="1") && (v2=="") && (v3!="")) {ret = true;}
	if ((v1=="1") && (v2=="") && (v3=="")) {ret = true;}
	if ((v1=="0") && (v2=="") && (v3=="")) {ret = true;}

	return ret;
}


function valider_5(presence_code_barre_mobile,saisie_code_barre_mobile) {
	ret = false;
	v1 = "0";
	v2 = "";


	if (presence_code_barre_mobile!="")    {v1 = presence_code_barre_mobile;}
	if (saisie_code_barre_mobile!="")    {v2 = saisie_code_barre_mobile;}

	/* test des informations */
	if ((v1=="1") && (v2!="")) {ret = true;}
	if ((v1=="0") && (v2=="")) {ret = true;}

	return ret;
}


function valider_6(presence_imei,saisie_imei) {
	ret = false;
	v1 = "0";
	v2 = "";


	if (presence_imei!="")    {v1 = presence_imei;}
	if (saisie_imei!="")    {v2 = saisie_imei;}

	/* test des informations */
	if ((v1=="1") && (v2!="")) {ret = true;}
	if ((v1=="0") && (v2=="")) {ret = true;}

	return ret;
}


function valider_7(presence_bulletin,j_accepte_de_recevoir) {
	ret = false;
	v1 = "0";
	v2 = "0";


	if (presence_bulletin!="")    {v1 = presence_bulletin;}
	if (j_accepte_de_recevoir!="")    {v2 = j_accepte_de_recevoir;}

	/* test des informations */
	if ((v1=="1") && (v2=="0")) {ret = true;}
	if ((v1=="1") && (v2=="1")) {ret = true;}
	if ((v1=="0") && (v2=="0")) {ret = true;}

	return ret;
}