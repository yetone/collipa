var superLove = function() {
  console.log("\n%c  \n", "font-size:100px; background:url(http://collipa.com/static/upload/avatar/1388055929_175x128.jpg) no-repeat 0px 0px;");

  return "You are my love."
}

var love = function() {
  /*
  var loveMessage = "瓦日瓦瓦瓦瓦毋毋瓦毋毋毋毋毋瓦瓦瓦毋瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦日日日日日日日日日日日日日日日日瓦瓦瓦己\n"+
                    "瓦瓦毋毋毋毋毋毋毋毋毋毋毋毋毋毋瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦日日日日日日日日日日日瓦瓦瓦瓦瓦瓦車鬼車瓦\n"+
                    "毋瓦毋毋毋毋毋毋毋毋毋毋毋瓦毋瓦瓦毋車車車毋毋毋毋瓦瓦瓦瓦瓦日日日日日日日日日日日日瓦瓦日瓦瓦毋瓦瓦\n"+
                    "瓦瓦毋毋毋毋毋毋毋毋毋毋毋瓦瓦車龠龍龍龍龍龠龠龍龍龠鬼瓦日瓦日日日己日己己己己日日日日日瓦瓦日瓦日己\n"+
                    "毋瓦毋毋毋毋毋毋毋毋瓦瓦瓦車馬龍齱齱齱齱齱龍龍龍龍齱龍馬瓦日日日日己己己己己己己日日日日日日毋瓦瓦日\n"+
                    "毋瓦毋毋毋毋毋毋毋瓦瓦瓦鬼龍齱龍龍龍龍龍龍龍龍龍龍龍龍龍龠毋日日日己己己己己己己日日日日日瓦毋瓦日己\n"+
                    "毋瓦毋毋毋毋毋毋毋瓦瓦鬼龍齱齱齱齱齱齱齱龍龍龍龍龍龍龍龍齱龍毋日日己己己己己己己己日日日日日毋瓦日己\n"+
                    "毋瓦毋毋毋毋毋毋毋瓦車龍齱龍齱齱齱齱齱齱齱龍龠龠龍龍龍龍龍龍龠瓦己己己己己乙乙乙己己己己己己日己己乙\n"+
                    "毋瓦毋毋毋毋毋毋瓦毋龠齱龍龍龍龍龍龍齱齱齱龍龍龠龍齱龍龍龍龍龍馬日己己己乙乙乙乙己己己己己己己乙乙十\n"+
                    "毋瓦毋毋毋毋毋毋瓦馬齱龍齱齱齱齱齱齱齱龍龍龍龍馬龠龍龍龍龍龍龍龠毋己己己乙乙乙乙乙己己己己己己乙乙十\n"+
                    "毋瓦毋毋毋毋毋毋毋龍齱龍龍齱齱齱齱齱齱齱龍龍龠馬馬馬龠龍龍龍龠龠鬼己己己乙乙乙乙乙乙己己己日日己己乙\n"+
                    "毋瓦毋毋毋毋毋瓦鬼齱龍龍齱齱齱齱龍龍馬馬鬼鬼車車車鬼馬龠龍龍龠馬馬瓦乙乙乙乙十十乙乙乙乙己己日己己乙\n"+
                    "毋瓦毋毋毋毋毋瓦馬齱龍齱龍齱齱龍馬車車毋毋毋毋毋毋車鬼馬龠龠龠馬馬瓦乙乙乙十十十十乙乙乙乙乙乙乙乙亅\n"+
                    "毋瓦毋毋毋毋毋毋馬龍龍龍龍龍龠鬼車毋毋毋毋毋毋毋毋毋車鬼馬龠馬馬鬼瓦乙乙十十十十十乙乙乙乙乙乙乙乙亅\n"+
                    "瓦瓦毋毋毋毋毋毋馬齱龍龍龍龠鬼車毋毋毋毋毋毋毋毋瓦瓦毋車鬼馬馬馬鬼毋乙乙十十十十十十乙乙乙乙乙乙十亅\n"+
                    "瓦瓦毋毋毋毋毋毋馬齱龍龍龍馬車車毋毋毋毋毋毋毋瓦瓦瓦毋毋車鬼鬼鬼鬼毋乙乙十十十十十十十十十乙己己乙亅\n"+
                    "日日毋毋毋毋毋瓦鬼龍龍龍龠鬼車毋毋毋毋毋瓦瓦瓦瓦瓦瓦毋毋毋車鬼鬼鬼毋乙乙十十十十十十十十十乙己日乙十\n"+
                    "己己毋毋毋毋毋瓦鬼龍龍龍馬車車毋毋毋瓦瓦瓦瓦瓦瓦瓦瓦毋毋車車車車鬼車己十十十十十十十十十十乙己乙十亅\n"+
                    "己己瓦毋毋毋毋毋鬼龍龍龍鬼鬼鬼鬼鬼鬼車毋毋毋毋毋車鬼鬼鬼鬼車毋車鬼車己十十十十十十十十十十十十亅十丶\n"+
                    "己乙瓦毋毋毋毋毋鬼龍龍馬車車鬼車車車鬼車毋毋毋毋車車車毋毋車毋毋鬼車己十十十十十十十十十亅十十十十丶\n"+
                    "己乙瓦毋毋毋毋瓦車龠龍馬車車車鬼馬馬車毋毋瓦瓦毋毋鬼馬鬼車毋毋毋車毋乙十十十十十十十亅亅亅十十亅十丶\n"+
                    "己乙日毋毋毋毋毋瓦鬼龠馬車毋車鬼鬼馬鬼車毋瓦瓦毋車車車車車毋瓦毋車瓦乙乙十十十十十十十亅亅亅亅亅亅丶\n"+
                    "己乙日毋毋毋毋毋瓦毋馬鬼車毋毋毋毋毋毋毋毋瓦瓦瓦瓦毋瓦瓦瓦瓦瓦毋毋日己乙乙乙十十十十亅亅亅亅亅亅亅丶\n"+
                    "乙乙日瓦毋毋毋毋瓦毋鬼鬼車毋毋毋瓦瓦瓦瓦瓦瓦瓦瓦日日日日日日瓦毋毋日己己己乙乙十十亅亅亅亅亅亅亅亅丶\n"+
                    "己乙己瓦毋毋毋毋毋瓦車鬼車毋毋毋瓦瓦瓦瓦瓦日日瓦日日日己己日日瓦瓦己己己己己乙乙十亅亅亅亅亅十十亅亅\n"+
                    "己乙己瓦毋毋毋毋瓦瓦毋車車車毋毋瓦瓦瓦瓦毋日日瓦瓦日己己己己日日己乙己己己己己乙十亅亅亅亅亅十十亅亅\n"+
                    "乙乙己瓦毋毋毋毋毋瓦瓦瓦毋車毋毋瓦瓦瓦毋毋瓦瓦瓦瓦日日己己己日己乙乙乙乙己己己乙十亅亅亅亅亅亅亅亅丶\n"+
                    "乙十己瓦毋毋毋毋毋瓦瓦瓦毋車車毋毋毋瓦毋車毋毋毋毋日日日日日日己十乙乙乙乙乙乙乙十亅亅亅亅亅亅丶丶　\n"+
                    "己乙己日瓦毋毋毋瓦瓦瓦瓦瓦車車毋毋毋瓦瓦瓦瓦瓦瓦瓦瓦日日日日日乙十十乙乙乙乙乙乙十亅亅亅亅亅十亅亅丶\n"+
                    "乙十己日瓦毋毋毋毋瓦瓦瓦瓦毋車毋毋毋車毋毋瓦瓦瓦毋毋毋瓦日瓦日乙十十十十十十乙乙乙十亅亅亅亅亅亅亅丶\n"+
                    "乙乙日瓦毋毋毋毋瓦瓦瓦瓦瓦瓦車車毋毋車鬼鬼車車車車車瓦瓦瓦瓦日乙乙十十十十十十十十十亅亅亅亅亅亅丶　\n"+
                    "乙乙日瓦毋毋毋毋瓦瓦瓦瓦瓦車鬼車車毋毋毋車毋毋毋毋瓦瓦瓦毋瓦己乙乙十十十亅十十十十十亅亅亅亅亅丶丶　\n"+
                    "乙乙日瓦毋毋毋毋瓦瓦瓦瓦瓦車鬼車車毋毋毋毋毋毋毋瓦瓦瓦毋毋己己乙乙十十亅亅亅亅亅十十十亅亅亅十十亅丶\n"+
                    "日己瓦毋毋毋毋毋瓦瓦瓦瓦瓦車馬車車車毋瓦瓦瓦瓦瓦瓦瓦瓦毋瓦己己乙乙十十亅亅亅亅亅十十十十亅十十十亅亅\n"+
                    "日己瓦毋毋毋毋毋瓦瓦瓦瓦瓦車龠車車車車毋瓦瓦瓦瓦瓦瓦毋毋瓦己己乙乙十十亅亅亅亅亅亅十十十十十乙十十亅\n"+
                    "日日毋毋毋毋毋毋瓦瓦瓦瓦日毋馬車毋車車車毋毋毋毋毋毋毋毋瓦己己乙乙十十亅亅亅亅亅亅亅十十十十十十十丶\n"+
                    "日瓦毋毋毋毋毋毋毋瓦瓦瓦日瓦鬼毋毋毋毋車車車車車毋毋瓦毋毋日己乙乙十十亅亅亅亅亅亅亅十十十十十十十丶\n"+
                    "乙瓦毋毋毋毋毋毋瓦瓦瓦日瓦毋車毋毋毋毋毋毋毋毋毋瓦瓦瓦毋毋毋瓦己乙乙十亅亅亅亅亅亅亅亅十十乙乙十乙亅\n"+
                    "己瓦毋毋毋毋毋毋瓦瓦瓦毋車車車毋毋毋瓦瓦瓦瓦瓦瓦瓦瓦瓦毋毋毋毋瓦日己己乙乙十亅亅亅亅亅十十十十十十亅\n"+
                    "日毋車車毋毋毋毋毋毋車車車毋毋毋瓦瓦瓦瓦瓦日日日日日瓦瓦瓦瓦瓦瓦日日瓦日己己乙十亅亅亅十十十十亅十丶\n"+
                    "瓦毋車車車車車鬼鬼鬼車車車毋毋瓦瓦瓦瓦日日日日日日日瓦瓦瓦瓦瓦日日日瓦日己己己乙亅亅亅亅亅十十十亅亅\n"+
                    "車毋車車車車馬馬馬鬼車車車毋毋瓦瓦日日日日日日日日日日日日日日日日日瓦日己己乙十亅亅亅亅亅十乙乙十十\n"+
                    "車車車車車車車鬼馬馬鬼毋毋毋瓦瓦瓦日日日日日日己己日日日日日日日日瓦瓦日己己己十亅亅亅亅亅亅乙乙十十\n"+
                    "鬼車鬼車車車毋毋車馬鬼車瓦瓦瓦日日日日日日日日己己己日日己己己日日瓦日日己己乙亅亅亅亅亅亅亅十十十亅\n"+
                    "鬼車鬼鬼車車車毋毋車鬼鬼車瓦日日日日日己己己己己己己己己己己己乙乙己乙十十亅亅亅亅亅亅亅亅十十十乙亅\n"+
                    "鬼車鬼鬼車車車車毋毋毋瓦瓦日日己己己己己己乙乙乙乙乙乙乙乙乙乙乙乙十十十十亅亅亅亅亅亅亅亅十己乙十十\n"+
                    "鬼車鬼車車車車車毋瓦瓦日日日己己己己乙乙乙乙乙乙乙乙乙乙乙乙十十十乙十十十亅亅亅亅亅亅亅亅亅亅亅亅丶\n"+
                    "鬼毋車車車車毋毋毋瓦日日己己乙乙乙十十十十十十十十十亅亅亅亅亅亅亅亅亅亅亅丶丶丶丶丶丶丶丶丶丶丶丶　";
  */
  var loveMessage = "\n　　　丶　　亅馬龠龠龠龍馬己　　　　　　乙毋瓦毋己日十　亅瓦鬼馬鬼馬馬鬼瓦丶丶毋瓦己車十　　　　　　\n"+
                    "　　　　　　丶馬龠龠鬼龠鬼　　　　　　　乙日日毋瓦日丶丶日車鬼鬼馬馬龠馬車瓦瓦車車瓦馬日　　　　　　\n"+
                    "丶　　丶丶　丶鬼龠龠龠龠馬丶　　　　　亅瓦瓦瓦車瓦毋瓦毋鬼馬龠馬龠龠龍龠龠龍龠馬車鬼龠瓦　　乙十　　\n"+
                    "丶　　丶十日丶亅車龍龠龠馬亅　　　丶十己車毋車毋日瓦車鬼馬龠龠馬龠龍龍龍龍龍龍龍馬鬼馬日亅毋鬼毋　　\n"+
                    "丶　丶亅乙車亅　乙毋馬馬鬼乙　　　丶乙毋毋毋鬼車車鬼馬龠龠龠馬車馬龠龠龠龍龍龍龍龍鬼乙丶乙車鬼鬼十　\n"+
                    "丶　亅毋車鬼十　　乙十十丶丶　　　　亅瓦毋毋毋車鬼馬龠龠龠馬鬼車鬼馬龠龠龠龍龍龍龍龠己亅鬼馬龠鬼亅丶\n"+
                    "丶　丶己馬車亅　丶十丶　　　　　　　亅己毋毋瓦車馬馬龠龠馬車毋毋鬼馬馬龠龍龍龍龍龍龍馬乙瓦毋車亅乙車\n"+
                    "亅　丶亅毋乙　丶丶乙十　丶丶丶丶丶丶丶亅己瓦車鬼馬龠馬馬毋瓦瓦瓦毋車鬼馬龠龍龍龍龍龍龍毋十丶十瓦馬龠\n"+
                    "十　丶亅車毋亅　丶毋瓦　丶丶丶丶丶丶　　亅日鬼馬龠馬鬼毋日日日日瓦瓦毋車鬼龠龍齱龍龍龍鬼毋車車馬龠馬\n"+
                    "亅　丶亅鬼鬼亅　　己乙　丶丶丶丶丶丶丶丶十瓦馬龠馬車瓦己己己日日日瓦瓦毋車馬龍齱齱龍齱龠鬼鬼瓦鬼龠馬\n"+
                    "十丶亅亅己日十乙乙日乙亅亅亅亅亅十十十十己車龠龍車日己己己己日日日日瓦毋車馬龠齱齱齱齱龍日十己毋馬馬\n"+
                    "日己日日瓦毋瓦瓦日瓦瓦己己己己己己乙乙乙日馬龍鬼日乙乙乙己己日日日日瓦毋車鬼龠龍齱齱齱齱瓦乙瓦車車龠\n"+
                    "毋瓦毋毋毋鬼毋瓦瓦毋瓦日日己己己己己己乙瓦龠龍瓦乙乙乙乙己己日日日瓦瓦毋車鬼馬龠齱齱齱齱馬馬馬毋鬼龠\n"+
                    "車毋瓦瓦瓦車車瓦瓦毋毋日日日日己日己己己毋龍龠己乙乙己己己己日日日日瓦毋車鬼馬龠齱齱齱齱龍鬼鬼毋車鬼\n"+
                    "車瓦瓦瓦日毋瓦日瓦瓦瓦日日日日日己己己己瓦馬鬼己乙乙乙己己己日日日瓦瓦毋車車鬼馬龍齱齱齱龍車車車車車\n"+
                    "鬼車鬼鬼鬼鬼鬼馬馬鬼鬼毋日瓦瓦毋瓦日日瓦日車車乙乙乙乙乙己己日日瓦瓦瓦毋鬼馬馬龠龍齱齱齱龍馬鬼車鬼車\n"+
                    "鬼毋車馬龠龍龍龍龍龠馬鬼車鬼車毋毋毋瓦車車車瓦乙乙己瓦毋瓦瓦日日瓦瓦車馬龠龠龠龠龠齱龍齱齱龠龠馬鬼鬼\n"+
                    "日日日鬼龍齱龍龍龍龍龠馬馬毋毋毋車毋毋車車瓦日十乙己日毋毋毋瓦瓦毋車鬼鬼車毋車馬龠龍龍龍龍馬龠鬼瓦車\n"+
                    "毋瓦瓦車龠龍龍龍齱齱龍車瓦己己乙乙乙乙毋車日日十十乙日瓦毋毋毋瓦毋鬼鬼車鬼龠龠龍龠龍龠龍龠毋毋日日己\n"+
                    "日己日日馬龍龍龍龍龍鬼己乙乙乙乙乙十乙日日己己十乙毋毋龍齱鬼毋日日車鬼馬龍齺龍龍龠龍馬龍鬼瓦瓦日日己\n"+
                    "日己日瓦瓦毋毋車毋毋瓦日己己己己乙乙己己己己乙十十乙己鬼馬鬼瓦乙己車車車鬼馬馬馬鬼龠馬龠瓦日瓦瓦日己\n"+
                    "毋瓦毋毋瓦瓦瓦日日日日日日己己己乙乙乙己己乙乙十十乙己瓦毋瓦己乙己毋毋毋毋車車車車龠龠鬼日日日瓦日己\n"+
                    "車毋毋瓦瓦瓦日日日日己己己乙乙乙乙乙乙己乙己己十十十乙己己己乙十己瓦毋瓦日日日瓦鬼龠鬼瓦日日日日日己\n"+
                    "瓦日瓦瓦瓦日日日日日日己己己己己乙乙己乙乙己己十十十乙乙己乙十十己瓦毋瓦日日日瓦馬馬瓦日日日日日日日\n"+
                    "毋瓦毋毋瓦瓦瓦瓦日日日己己己己乙乙乙乙乙乙己乙乙十十乙己己日十十乙日毋車瓦日瓦車龠車瓦日日日日日日日\n"+
                    "車毋毋毋瓦瓦瓦瓦日日日己己己己乙乙乙乙乙乙乙乙乙十乙乙己瓦瓦十十乙日瓦鬼車瓦毋鬼馬毋日日日日日日日日\n"+
                    "車毋毋毋毋瓦瓦瓦日日日日己己己己乙乙己乙乙乙乙乙乙己日瓦車瓦己己日瓦車鬼鬼車車馬鬼瓦日日日日日日日日\n"+
                    "車毋毋毋毋瓦瓦瓦瓦日日日己己己己乙乙己乙乙乙乙乙乙乙日毋車日己瓦毋鬼馬鬼馬鬼鬼馬毋日日日日日日日日日\n"+
                    "車毋車毋毋毋瓦瓦瓦日日日己己己己乙乙己乙乙乙乙乙己己己瓦毋毋日瓦毋鬼馬龠馬車馬車日日日日日日日日瓦日\n"+
                    "鬼車車毋毋毋瓦瓦瓦日日日己己己己己乙己乙乙乙乙乙己己己己己日瓦毋車鬼龠馬車鬼鬼瓦己日日日日日日瓦瓦瓦\n"+
                    "鬼車車車毋毋毋瓦瓦瓦日日日己己己己己己己己己乙己己乙乙乙己己日毋車鬼鬼車鬼鬼毋日己日日日日日瓦瓦瓦瓦\n"+
                    "鬼車車車車毋毋瓦瓦瓦瓦日日日己己己己己己乙乙十十十乙十十己己己毋車車車車鬼鬼車日日日日日日瓦瓦瓦毋瓦\n"+
                    "鬼鬼鬼車車車毋毋毋瓦瓦瓦日日日己己己乙十十亅十十十十十十乙己己日瓦毋毋鬼馬馬鬼瓦日日日瓦瓦瓦瓦毋毋毋\n"+
                    "馬鬼鬼鬼鬼車車毋毋毋瓦瓦日日日日己十十十十十十十乙十十十乙乙己日瓦毋車馬馬馬鬼毋日己日瓦瓦瓦毋毋毋毋\n"+
                    "馬鬼馬鬼鬼鬼車車毋毋瓦瓦日日日己十十乙十十十十十乙十十十乙乙己日日毋鬼鬼鬼鬼車車瓦日己日瓦毋毋毋毋毋\n"+
                    "馬馬馬馬鬼鬼車車毋毋毋瓦日日日己十乙乙十十十十十乙十十十乙己己己瓦車車毋毋車車毋瓦日日己日瓦毋車車毋\n"+
                    "龠馬馬馬鬼鬼鬼車車毋毋瓦瓦日日乙乙乙十十乙十十乙乙十十十十乙乙己瓦瓦瓦瓦瓦瓦瓦瓦瓦日己己己己日瓦毋車\n"+
                    "龠馬馬馬馬鬼鬼車車毋毋瓦瓦瓦己乙己乙十乙十十乙乙乙乙十十乙乙十乙己日日日日日瓦瓦瓦日日日日瓦瓦瓦毋毋\n"+
                    "龠馬龠馬馬馬鬼鬼車車毋毋瓦日乙己己乙十乙十乙乙乙乙己乙十十乙乙乙乙己日日日瓦瓦日日日瓦瓦瓦車鬼馬馬鬼\n"+
                    "龠龠龠龠馬馬鬼鬼鬼車毋毋毋己己日己十乙十十乙乙己乙乙己乙十乙乙乙己日瓦瓦瓦日日日瓦日日瓦毋車毋毋毋瓦\n"+
                    "龍龠龠龠龠馬馬鬼鬼車車車毋日日日乙十乙十乙乙乙己乙乙己己乙乙己日瓦瓦瓦瓦日日日日日己瓦車毋毋毋瓦瓦日\n"+
                    "龍龠龠龠龠馬馬馬鬼鬼鬼車車毋瓦日乙十乙十己乙己己乙乙乙己己日瓦瓦瓦瓦瓦日日瓦日日日日毋毋瓦瓦瓦日瓦瓦\n"+
                    "龍龍龍龠龠龠龠馬馬馬鬼鬼車車毋瓦乙十十乙己乙日己乙己己己日日瓦瓦瓦瓦瓦日日日日瓦瓦瓦毋瓦瓦瓦瓦瓦瓦瓦\n"+
                    "龍龍龍龍龠龠龠龠龠馬馬鬼鬼鬼車瓦乙十乙己己乙日己乙己己己日日瓦瓦瓦瓦瓦日日己瓦車瓦瓦瓦瓦瓦瓦瓦毋毋瓦\n"+
                    "齱龍龍龍龍龍龠龠龠龠馬馬馬馬鬼瓦十十乙日己己瓦日乙己日己己日瓦毋毋瓦日日己瓦車車日毋瓦瓦瓦毋毋毋車毋\n"+
                    "齱龍龍龍龍龍龍龍龠龠龠龠龠馬馬瓦十十己日己己毋瓦己己日日己瓦毋瓦瓦日己己瓦車鬼毋瓦毋瓦瓦瓦車車車車毋\n"+
                    "齱齱齱齱龍龍龍龍龍龍龠龠龠龠龠瓦乙亅己日己日瓦瓦日己日己日日日己己己日毋鬼鬼鬼毋瓦毋瓦瓦車鬼毋毋車車\n"+
                    "齱齱齱齱齱齱龍龍龍龍龍龍龠龠龠日乙乙十日日日瓦毋日日日己己己己己己瓦車鬼鬼馬鬼毋毋車毋車鬼毋毋車車車\n"+
                    "齱齱齱齱齱齱齱龍龍龍龍龍龍龍鬼乙己日十十日日瓦毋瓦日瓦瓦瓦毋毋毋車鬼鬼鬼馬馬鬼毋毋鬼鬼馬車瓦車瓦日日\n"+
                    "齺齱齱齱齱齱齱齱龍龍龍龍龍龍瓦乙日日日亅亅己日瓦瓦日日瓦車車鬼鬼鬼鬼鬼鬼鬼鬼車毋車馬馬馬車毋瓦日日日\n";

  console.log(loveMessage);

  return "You are my love.";
};

var get_cookie = function(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r?r[1]:undefined;
  },

  mousePosition = function(e) {
    if (e.pageX && e.pageY) {
      return {x: e.pageX, y: e.pageY};
    }
    return {
      x: e.clientX + document.body.scrollLeft - document.body.clientX,
      y: e.clientY + document.body.scrollTop - document.body.clientY
    };
  },

  popup = function($popdiv, pos) {
    if (!pos) {
      pos = 'absolute';
    }
    var _scrollHeight = $(document).scrollTop(),
        _windowHeight = $(window).height(),
        _windowWidth  = $(window).width(),
        _popdivHeight = $popdiv.height(),
        _popdivWidth  = $popdiv.width();

    _popTop = (_windowHeight - _popdivHeight) / 2;
    _popLeft = (_windowWidth - _popdivWidth) / 2;
    $popdiv.css({'left': _popLeft + 'px', 'top': _popTop + 'px', 'display': 'block', 'position': pos});
    if ($popdiv.width() + 2 >= _windowWidth) {
      $popdiv.width(_windowWidth * 0.85);
    }
  },

  repel = function(data) {
    var buff;
    if (data.parent('li').hasClass('up')) {
      buff = '.down a';
    } else if (data.parent('li').hasClass('down')) {
      buff = '.up a';
    } else {
      return false;
    }
    var $this = data.parents('ul.vote').find(buff),
        content = $this.html(),
        content_top = content.substr(0, content.indexOf('</i>') + 4),
        content_tail = content.substr(content.indexOf('</i>') + 5, content.length),
        count = parseInt(content.substr(content.indexOf('(') + 1, content.indexOf(')')));

    if (content.indexOf('已') !== -1) {
      $this.parent('li').removeClass('pressed');
      content_tail = content.substr(content.indexOf('已') + 1, content.length);
      content = content_top + ' ' + content_tail;
      if (count > -1) {
        count -= 1;
        content_top = content.substr(0, content.indexOf('('));
        content = content_top + "(" + count + ")";
      }
      $this.html(content);
    }
  },

  $D = $(document),
  $W = $(window),

  noty = function(data, static) {
    var noty_div;
    if (!data) {
      noty_div =
        '<div id="noty" class="info">'
      +   "您操作过快，服务器未响应"
      + '</div>';
    } else if (data.status) {
      noty_div =
        '<div id="noty" class="' + data.status + '">'
      +   data.message
      + '</div>';
    }

    $('#noty').remove();
    $('body').append(noty_div);
    popup($('#noty'), 'fixed');
    if (!static) {
      setTimeout(function() {$('#noty').fadeOut(1200);}, 600);
    } else {
      $('#noty').addClass('static');
    }
  };

$(function() {
  $.fn.extend({
    fix: function() {
      var $nav = this,
          make_fix = function($nav) {
            var top = $(document).scrollTop(),
                menu_top,
                $shape = $('#shape'),
                $nav_fixed = $($nav.selector + '.fixed'),
                $menu = $('#head .menu'),
                $menu_fixed = $('#head .menu.fixed'),
                $head = $('#head'),
                nav_top = $nav.offset().top,
                nav_width = $nav.width(),
                nav_height = $nav.height(),
                menu_left = $menu.offset().left,
                menu_height = $menu.height(),
                head_left = $head.offset().left;
            if (top >= nav_top) {
              if (!$nav_fixed.length) {
                menu_top = (parseInt(nav_height) - parseInt(menu_height)) / 2;
                $nav_fixed = $nav.clone();
                $nav_fixed.addClass('fixed').css({'width': nav_width});
                $nav.after($nav_fixed);
                if ($('#head .menu.fixed').length) {
                  $('#head .menu.fixed').remove();
                }
                $menu_fixed = $menu.clone();
                $menu_fixed.addClass('fixed').css({'right': +head_left + 20 + 'px', 'top': menu_top + 'px'});
                $menu_fixed.insertAfter($menu).hide().fadeIn(600);
              }
            } else {
              $nav_fixed.remove();
              $menu_fixed.remove();
            }
          };
      if (!$nav || $nav.length === 0) {
        return;
      } else {
        make_fix($nav);
        $(document).on('scroll', function() {
          make_fix($nav);
        });
      }
    },
    tooltip: function() {
      this.each(function(i, v) {
        var $v = $(v);
        $v.off('mousemove').off('mouseout');
        $v.on('mousemove', function(e) {
          var text = $(v).attr('data-tooltip');
          if (!$('.tooltip').length) {
            var tooltip = '<div class="tooltip"></div>';
            $(tooltip).appendTo('body').fadeIn();
          }
          $('.tooltip').css({'position': 'absolute',
                             'top': mousePosition(e).y + 15,
                             'left': mousePosition(e).x + 15
          }).html(text);
        }).on('mouseout', function(e) {
          $('.tooltip').fadeOut(150);
          setTimeout(function() {$('.tooltip').remove();}, 150);
        });
      });
    },
    navBottomPosition: function(duration) {
      var fp = function($nav) {
        if (!$nav || $nav.length ===0) {
          return;
        }
        var w = $nav.width(),
            l = $nav.position().left,
            $navSpan = $nav.parents('.nav-wrap').find('.nav-bottom-span'),
            nw = $navSpan.width(),
            nl = $navSpan.position().left;
        // duration = Math.abs((nl + nw) - (l + w)) * 2;
        duration = 300;
        if (nw === 0) {
          $navSpan.hide().css({'left': l, 'width': w}).fadeIn(300);
        } else {
          $navSpan.stop();
          $navSpan.animate({'left': l, 'width': w}, duration);
        }
      },
      timer;

      fp($(this.selector + '.on'));
      $(document).on('mouseover', this.selector, function() {
        clearTimeout(timer);
        fp($(this));
      }).on('mouseout', this.selector, function() {
        timer = setTimeout(function() {
          fp($($(this).selector + '.on'));
        }, 130);
      });
    },
    pjax: function(opt) {
      opt = $.extend({
        event: 'click',
        container: '#pjax-content',
        part: '#pjax-content'
      }, opt);

      $(document).on(opt.event, this.selector, function(e) {
        e.preventDefault();
        var $this = $(this),
            $pjaxContent = $(opt.container),
            func = function(opt) {
              var $ploading = $('<span class="ploading style-2"></span>');
              if (!$('.ploading').length) {
                $('body').append($ploading);
              }
              $.ajax({
                url: $this.attr('href'),
                type: 'GET',
                dataType: 'html',
                success: function(d) {
                  var state = {
                        title: '',
                        html: $pjaxContent.html(),
                      },
                      $ploading = $('.ploading');
                  $ploading.animate(
                    {opacity: 0},
                    function() {
                      $ploading.remove();
                    }
                  );
                  $pjaxContent.html($(d).find(opt.part).html());
                  //$('#script-block').html($(d).find('#script-block').html());
                  //$('title').text($(d).find('title').text());
                  History.pushState(state, document.title, opt.url);
                  if (opt.success) {
                    opt.success(d);
                  }
                }
              });
            };
        window.addEventListener('popstate', function(e) {
          var state = History.getState();
          console.log(state);
          if (state.data.html) {
            $('#pjax-content').html(state.data.html);
          }
        });
        if (opt.cbk) {
          opt.cbk();
        }
        func(opt);
      });
          /*
          History.Adapter.bind(window, 'popstate', function() {
            var state = History.getState();
            console.log(state);
            if (state) {
              $('#pjax-content').html(state.data.html);
            }
          });
          */
    }
  });
  var shape_resize = function(data) {
    var window_height = $(window).height(),
        window_width = $(window).width(),
        shape_width = $('#shape').width(),
        min_width = window_width <= shape_width ? window_width : shape_width;

    if (window_width === min_width) {
      $('#shape').addClass('mobile').css({'width': window_width});
      var $imgs = $('.content img');
      $imgs.each(function() {
        if ($(this).width() > min_width) {
          $(this).css({"max-width": min_width - 20 + 'px'});
        }
      });
    } else {
      $('#shape').removeClass('mobile').css({'width': '720px'});
    }
    if (data) {
      var $head = $('#head'),
          $menu_fixed = $('#head > .menu.fixed'),
          $nav = $('.nav'),
          head_left = $head.offset().left;
      $nav.css({'width': min_width - 20 + 'px'});
      $menu_fixed.css({'right': +head_left + 20 + 'px'});
    }
  };

  $('.body-nav').fix();
  $('.nav li').navBottomPosition();

  shape_resize();

  $(window).resize(function() {
    if ($('#head > .menu.fixed').length) {
      shape_resize(true);
    } else {
      shape_resize();
    }
  });

  $D.on('click', '.layout-close', function(e) {
    e.preventDefault();
    $('#layout').fadeOut();
  });

  $D.live('keypress', function(e) {
    if (e.ctrlKey && e.which == 13 || e.which == 10) {
      $('form button').click();
    }
  });

  $D.click(function() {
    var $d = $('#noty.static');
    $d.fadeOut(1200);
  });

  if (notify.permissionLevel() === notify.PERMISSION_DEFAULT) {
    var html = '<div id="open-notification" class="tc"><a href="#;">点我开启桌面提醒</a></div>';
    $('body').prepend(html);
  }

  $D.on('click', '#open-notification a', function() {
    notify.requestPermission(function(){
      if (notify.permissionLevel() === notify.PERMISSION_GRANTED) {
        $('#open-notification').remove();
      }
    });
  });

  function Notifier() {
  }
  Notifier.prototype.notify = function(title, options) {
    var n;
    if (window.webkitNotifications) {
      n = window.webkitNotifications.createNotification(options.icon, title, options.body);
      n.onclick = function() {
        window.focus();
        this.cancel();
      };
      n.show();
    } else if (navigator.mozNotification) {
    }
  };
  notifier = new Notifier();

  $D.click(function() {
    var $d = $('.open.menu-list');
    $d.removeClass('open');
  });

  var cslMessage = "             ___    ___                            \n"+
                   "            /\\_ \\  /\\_ \\    __                     \n"+
                   "  ___    ___\\//\\ \\ \\//\\ \\  /\\_\\  _____      __     \n"+
                   " /'___\\ / __`\\\\ \\ \\  \\ \\ \\ \\/\\ \\/\\ '__`\\  /'__`\\   \n"+
                   "/\\ \\__//\\ \\L\\ \\\\_\\ \\_ \\_\\ \\_\\ \\ \\ \\ \\L\\ \\/\\ \\L\\.\\_ \n"+
                   "\\ \\____\\ \\____//\\____\\/\\____\\\\ \\_\\ \\ ,__/\\ \\__/.\\_\\\n"+
                   " \\/____/\\/___/ \\/____/\\/____/ \\/_/\\ \\ \\/  \\/__/\\/_/\n"+
                   "                                   \\ \\_\\           \n"+
                   "                                    \\/_/           \n"+
                   "\n联系方式：i@yetone.net";
  window.console && console.info && console.info(cslMessage);
});
