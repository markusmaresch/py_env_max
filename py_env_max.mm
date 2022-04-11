<map version="freeplane 1.9.8">
<!--To view this file, download free mind mapping software Freeplane from https://www.freeplane.org -->
<node TEXT="py_env_max" FOLDED="false" ID="ID_1558508256" CREATED="1568633597132" MODIFIED="1649591680210"><hook NAME="MapStyle" zoom="1.1">
    <properties edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" fit_to_viewport="false" show_icon_for_attributes="true" show_note_icons="true"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node" STYLE="oval" UNIFORM_SHAPE="true" VGAP_QUANTITY="24 pt">
<font SIZE="24"/>
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="default" ID="ID_271890427" ICON_SIZE="12 pt" COLOR="#000000" STYLE="fork">
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="200" DASH="" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_271890427" STARTARROW="DEFAULT" ENDARROW="NONE"/>
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
<richcontent CONTENT-TYPE="plain/auto" TYPE="DETAILS"/>
<richcontent TYPE="NOTE" CONTENT-TYPE="plain/auto"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.attributes">
<font SIZE="9"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.note" COLOR="#000000" BACKGROUND_COLOR="#ffffff" TEXT_ALIGN="LEFT"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.selection" BACKGROUND_COLOR="#4e85f8" BORDER_COLOR_LIKE_EDGE="false" BORDER_COLOR="#4e85f8"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important" ID="ID_67550811">
<icon BUILTIN="yes"/>
<arrowlink COLOR="#003399" TRANSPARENCY="255" DESTINATION="ID_67550811"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000" STYLE="oval" SHAPE_HORIZONTAL_MARGIN="10 pt" SHAPE_VERTICAL_MARGIN="10 pt">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#0033ff">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#00b439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#990000">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#111111">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,5"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,6"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,7"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,8"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,9"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,10"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,11"/>
</stylenode>
</stylenode>
</map_styles>
</hook>
<node TEXT="Database" POSITION="right" ID="ID_512964669" CREATED="1649591232695" MODIFIED="1649619306307">
<node TEXT="Tables" ID="ID_1372701864" CREATED="1649620461125" MODIFIED="1649620469113">
<node TEXT="Config" ID="ID_922357515" CREATED="1649620457164" MODIFIED="1649620460450"/>
<node TEXT="Packages" ID="ID_2092545" CREATED="1649620473286" MODIFIED="1649620476233"/>
</node>
</node>
<node TEXT="Concept" POSITION="right" ID="ID_267867978" CREATED="1649615136559" MODIFIED="1649615139203">
<node TEXT="always ONE environment present or assumed" ID="ID_59735333" CREATED="1649615141059" MODIFIED="1649615159475"/>
</node>
<node TEXT="Options" POSITION="right" ID="ID_576269167" CREATED="1649591223570" MODIFIED="1649591226362">
<node TEXT="-env" ID="ID_1317793865" CREATED="1649591270732" MODIFIED="1649591275986">
<node TEXT="[-name env_name]" ID="ID_1839600931" CREATED="1649592535290" MODIFIED="1649592557698">
<node TEXT="# default name of environment py_env_&lt;yyyymm&gt;" ID="ID_1132368446" CREATED="1649592558639" MODIFIED="1649592662556">
<font BOLD="false"/>
</node>
<node TEXT="# override, if needed" ID="ID_1519875104" CREATED="1649592558639" MODIFIED="1649592750937">
<font BOLD="false"/>
</node>
</node>
<node TEXT="-init (from scratch)" ID="ID_1322610130" CREATED="1649591368269" MODIFIED="1649591383323">
<node TEXT="?" ID="ID_925303945" CREATED="1649594040771" MODIFIED="1649594042246"/>
<node TEXT="# boot strap a new environment from scratch" ID="ID_1378459813" CREATED="1649592752995" MODIFIED="1649592790470"/>
</node>
<node TEXT="-import (to database)" ID="ID_1850124847" CREATED="1649591284648" MODIFIED="1649591724223">
<node TEXT="# read existing and good environment into data base" ID="ID_788028655" CREATED="1649592792966" MODIFIED="1649592819867"/>
</node>
</node>
<node TEXT="-req" ID="ID_1240756931" CREATED="1649591308003" MODIFIED="1649591312459">
<node TEXT="-export" ID="ID_1545604522" CREATED="1649591312908" MODIFIED="1649591315496">
<node TEXT="# export requirements_&lt;yyyymm&gt;.txt" ID="ID_80233852" CREATED="1649592824613" MODIFIED="1649592851401"/>
<node TEXT="[-linux|-osx|-windows]" LOCALIZED_STYLE_REF="default" ID="ID_945021440" CREATED="1648840754952" MODIFIED="1649102752775" COLOR="#000000" BACKGROUND_COLOR="#ffffff" STYLE="fork">
<font BOLD="false"/>
<edge STYLE="bezier" COLOR="#808080"/>
</node>
</node>
<node TEXT="-import" ID="ID_86736026" CREATED="1649591395832" MODIFIED="1649591398286">
<node TEXT="# update/extend database from other requirements.txt" ID="ID_1803090562" CREATED="1649592871999" MODIFIED="1649592912410"/>
</node>
</node>
<node TEXT="-yml" ID="ID_827419953" CREATED="1649591320333" MODIFIED="1649591323349">
<node TEXT="-export" ID="ID_1134308203" CREATED="1649591323719" MODIFIED="1649591326150">
<node TEXT="# export environment_&lt;yyyymm&gt;.yml" ID="ID_1157909728" CREATED="1649592824613" MODIFIED="1649592974409"/>
<node TEXT="[-linux|-osx|-windows]" LOCALIZED_STYLE_REF="default" ID="ID_764191577" CREATED="1648840754952" MODIFIED="1649102752775" COLOR="#000000" BACKGROUND_COLOR="#ffffff" STYLE="fork">
<font BOLD="false"/>
<edge STYLE="bezier" COLOR="#808080"/>
</node>
</node>
<node TEXT="-import" ID="ID_1166130351" CREATED="1649591390826" MODIFIED="1649591394831">
<node TEXT="# update/extend database from other environment.yml" ID="ID_752214196" CREATED="1649592871999" MODIFIED="1649592943809"/>
</node>
</node>
<node TEXT="-cmds" ID="ID_885157960" CREATED="1649591459721" MODIFIED="1649591471467">
<node TEXT="-export" ID="ID_1932368402" CREATED="1649591471758" MODIFIED="1649591474448">
<node TEXT="create batch/shell scripts, build_&lt;yyyymm&gt;_0N_&lt;a-f&gt;.ext" ID="ID_1996910313" CREATED="1649593001802" MODIFIED="1649593080734">
<node TEXT="# M Levels" ID="ID_118788360" CREATED="1649593089553" MODIFIED="1649593094807"/>
<node TEXT="# up to N packages per level" ID="ID_1973847670" CREATED="1649593096100" MODIFIED="1649593112144"/>
</node>
<node TEXT="[-max N]" ID="ID_902090156" CREATED="1649592984387" MODIFIED="1649593000611"/>
<node TEXT="[-sh|-bat]" LOCALIZED_STYLE_REF="default" ID="ID_505539982" CREATED="1648840754952" MODIFIED="1649591504272" COLOR="#000000" BACKGROUND_COLOR="#ffffff" STYLE="fork">
<font BOLD="false"/>
<edge STYLE="bezier" COLOR="#808080"/>
</node>
</node>
</node>
<node TEXT="-package" LOCALIZED_STYLE_REF="default" ID="ID_808475736" CREATED="1649101683605" MODIFIED="1649102752772" COLOR="#000000" BACKGROUND_COLOR="#ffffff" STYLE="fork">
<font BOLD="false"/>
<edge COLOR="#808080"/>
<node TEXT="-add P" LOCALIZED_STYLE_REF="default" ID="ID_512273540" CREATED="1649101691435" MODIFIED="1649593263323" COLOR="#000000" STYLE="fork">
<font BOLD="false"/>
<edge STYLE="bezier" COLOR="#808080"/>
<node TEXT="# call: pip check" ID="ID_350357728" CREATED="1649593165660" MODIFIED="1649593175853"/>
<node TEXT="# call: pip install .. and check sucess" ID="ID_1598755260" CREATED="1649593122392" MODIFIED="1649593164648"/>
<node TEXT="# call: pip check" ID="ID_1466786505" CREATED="1649593140178" MODIFIED="1649593148662"/>
<node TEXT="# update database" ID="ID_1705602847" CREATED="1649593149234" MODIFIED="1649593155355"/>
</node>
<node TEXT="{-rm | -remove | -delete} P" LOCALIZED_STYLE_REF="default" ID="ID_857979055" CREATED="1649101695812" MODIFIED="1649593247516" COLOR="#000000" BACKGROUND_COLOR="#ffffff" STYLE="fork">
<font BOLD="false"/>
<edge STYLE="bezier" COLOR="#808080"/>
<node TEXT="# call: pip check" ID="ID_176542119" CREATED="1649593140178" MODIFIED="1649593148662"/>
<node TEXT="# warn, if P is dependency of other" ID="ID_928880018" CREATED="1649593204349" MODIFIED="1649593230112"/>
<node TEXT="# call: pip uninstall P" ID="ID_315330261" CREATED="1649593269824" MODIFIED="1649593277970"/>
<node TEXT="# call: pip check" ID="ID_1540657555" CREATED="1649593140178" MODIFIED="1649593148662"/>
<node TEXT="# update database" ID="ID_1447342363" CREATED="1649593149234" MODIFIED="1649593155355"/>
</node>
</node>
<node TEXT="-subset P0 P1 P2 .. Pn" ID="ID_1453385721" CREATED="1649593305566" MODIFIED="1649593532404">
<node TEXT="[-name subset]" ID="ID_35328711" CREATED="1649593475937" MODIFIED="1649593553429">
<node TEXT="# default name of subset py_env_&lt;yyyymm&gt;_subset" ID="ID_911315223" CREATED="1649593503354" MODIFIED="1649593586088"/>
<node TEXT="# override, if needed" ID="ID_680146717" CREATED="1649593588562" MODIFIED="1649593597023"/>
</node>
<node TEXT="# extract P0..Pn with all dependencies" ID="ID_1562506979" CREATED="1649593335435" MODIFIED="1649593449242"/>
</node>
<node TEXT="-update" ID="ID_1208640819" CREATED="1649594045677" MODIFIED="1649594056377">
<node TEXT="-latest-versions" ID="ID_382657485" CREATED="1649594065735" MODIFIED="1649619211682">
<node TEXT="# get latest versions from Pypi, and store in records" ID="ID_1024694016" CREATED="1649619216953" MODIFIED="1649619237979"/>
</node>
<node TEXT="-auto" ID="ID_1348387512" CREATED="1649594062102" MODIFIED="1649594064477">
<node TEXT="# try carefully updating out of date and not locked packages" ID="ID_496920381" CREATED="1649619245854" MODIFIED="1649619267298">
<node TEXT="complicated" ID="ID_855543586" CREATED="1649619269152" MODIFIED="1649619272945"/>
<node TEXT="can fail" ID="ID_1728926041" CREATED="1649619273304" MODIFIED="1649619275724"/>
</node>
</node>
</node>
<node TEXT="-statistics" ID="ID_1728840809" CREATED="1649615070978" MODIFIED="1649615077251">
<node TEXT="# name" ID="ID_1789245924" CREATED="1649615697984" MODIFIED="1649615700696"/>
<node TEXT="# last checked" ID="ID_1391117682" CREATED="1649615701077" MODIFIED="1649615705095"/>
<node TEXT="# num packages" ID="ID_669766446" CREATED="1649615079895" MODIFIED="1649615088766">
<node TEXT="of which also in %" ID="ID_1757927779" CREATED="1649615468464" MODIFIED="1649615529394"/>
<node TEXT="by levels" ID="ID_1526371611" CREATED="1649615472537" MODIFIED="1649615477431">
<node TEXT="level 1" ID="ID_368298714" CREATED="1649615089225" MODIFIED="1649615093907"/>
<node TEXT=".." ID="ID_961429854" CREATED="1649615094177" MODIFIED="1649615096158"/>
<node TEXT="level N" ID="ID_1812783307" CREATED="1649615096494" MODIFIED="1649615099883"/>
</node>
<node TEXT="by uptodateness" ID="ID_1301431307" CREATED="1649615557327" MODIFIED="1649615566788">
<node TEXT="# uptodate" ID="ID_1142243160" CREATED="1649615101615" MODIFIED="1649615109199"/>
<node TEXT="# locked" ID="ID_247498702" CREATED="1649615112663" MODIFIED="1649615115735"/>
<node TEXT="# updateable" ID="ID_275595498" CREATED="1649615116848" MODIFIED="1649615121754"/>
</node>
</node>
</node>
</node>
</node>
</map>
