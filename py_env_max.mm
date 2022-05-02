<map version="freeplane 1.9.13">
<!--To view this file, download free mind mapping software Freeplane from https://www.freeplane.org -->
<node TEXT="py_env_max" FOLDED="false" ID="ID_1558508256" CREATED="1568633597132" MODIFIED="1649591680210"><hook NAME="MapStyle" zoom="1.5">
    <properties show_icon_for_attributes="true" edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" show_note_icons="true" fit_to_viewport="false"/>

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
<node TEXT="Options" POSITION="right" ID="ID_1154867364" CREATED="1651431717138" MODIFIED="1651431721560">
<node TEXT="Flags" ID="ID_1399099359" CREATED="1651431566870" MODIFIED="1651431716194">
<node TEXT="--force" ID="ID_1839888695" CREATED="1651431572067" MODIFIED="1651431822170"/>
<node TEXT="--env ENV" ID="ID_1495297248" CREATED="1651431519496" MODIFIED="1651431816996">
<node TEXT="# environment name, overriding &lt;default&gt;" ID="ID_412878382" CREATED="1651431530093" MODIFIED="1651431553281"/>
</node>
</node>
<node TEXT="Actions" ID="ID_1986681682" CREATED="1651431728208" MODIFIED="1651431732405">
<node TEXT="--statistics" FOLDED="true" ID="ID_1728840809" CREATED="1649615070978" MODIFIED="1651515308366">
<icon BUILTIN="button_ok"/>
<node TEXT="# name" ID="ID_1789245924" CREATED="1649615697984" MODIFIED="1649615700696"/>
<node TEXT="# last checked" ID="ID_1391117682" CREATED="1649615701077" MODIFIED="1649615705095"/>
<node TEXT="# num packages" FOLDED="true" ID="ID_669766446" CREATED="1649615079895" MODIFIED="1649615088766">
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
<node TEXT="--env_init" ID="ID_132844671" CREATED="1651432213292" MODIFIED="1651432220133">
<node TEXT="# boot strap a new environment from scratch" ID="ID_1378459813" CREATED="1649592752995" MODIFIED="1649592790470"/>
<node TEXT="# only printed commands" ID="ID_1065759118" CREATED="1651432308671" MODIFIED="1651432320429"/>
</node>
<node TEXT="--env_import" ID="ID_1605793159" CREATED="1651431124899" MODIFIED="1651518242001">
<icon BUILTIN="button_ok"/>
<node TEXT="# read existing and good environment into data base" ID="ID_788028655" CREATED="1649592792966" MODIFIED="1649592819867"/>
<node TEXT="Enhancements" FOLDED="true" ID="ID_46448683" CREATED="1651515314405" MODIFIED="1651518237435">
<icon BUILTIN="idea"/>
<node TEXT="speedup" ID="ID_945268510" CREATED="1651515319277" MODIFIED="1651515323058">
<node TEXT="check, if env is uptodate on file system" ID="ID_1827809391" CREATED="1651518210510" MODIFIED="1651518229558"/>
</node>
</node>
</node>
<node TEXT="--upd_all" ID="ID_1652064161" CREATED="1651432044720" MODIFIED="1651432049839">
<node TEXT="-latest-versions" FOLDED="true" ID="ID_382657485" CREATED="1649594065735" MODIFIED="1649619211682">
<node TEXT="# get latest versions from Pypi, and store in records" ID="ID_1024694016" CREATED="1649619216953" MODIFIED="1649619237979"/>
</node>
<node TEXT="-all" FOLDED="true" ID="ID_1348387512" CREATED="1649594062102" MODIFIED="1651425249124">
<node TEXT="# try carefully updating out of date, with minimal conflichts" ID="ID_496920381" CREATED="1649619245854" MODIFIED="1651425266315">
<node TEXT="complicated" ID="ID_855543586" CREATED="1649619269152" MODIFIED="1649619272945"/>
<node TEXT="can fail" ID="ID_1728926041" CREATED="1649619273304" MODIFIED="1649619275724"/>
</node>
</node>
</node>
<node TEXT="--upd_scripts" ID="ID_1978411996" CREATED="1651432050356" MODIFIED="1651432055903">
<node TEXT="create batch/shell scripts, build_&lt;yyyymm&gt;_0N_&lt;a-f&gt;.ext" FOLDED="true" ID="ID_1996910313" CREATED="1649593001802" MODIFIED="1649593080734">
<node TEXT="# M Levels" ID="ID_118788360" CREATED="1649593089553" MODIFIED="1649593094807"/>
<node TEXT="# up to N packages per level" ID="ID_1973847670" CREATED="1649593096100" MODIFIED="1649593112144"/>
</node>
<node TEXT="[-max N]" ID="ID_902090156" CREATED="1649592984387" MODIFIED="1649593000611"/>
<node TEXT="[-sh|-bat]" LOCALIZED_STYLE_REF="default" ID="ID_505539982" CREATED="1648840754952" MODIFIED="1649591504272" COLOR="#000000" BACKGROUND_COLOR="#ffffff" STYLE="fork">
<font BOLD="false"/>
<edge STYLE="bezier" COLOR="#808080"/>
</node>
</node>
<node TEXT="--req_import" ID="ID_1123887930" CREATED="1651432056602" MODIFIED="1651432060595">
<node TEXT="# update/extend database from other requirements.txt" ID="ID_1803090562" CREATED="1649592871999" MODIFIED="1649592912410"/>
</node>
<node TEXT="--req_export" ID="ID_1307942704" CREATED="1651432069683" MODIFIED="1651524069890">
<icon BUILTIN="button_ok"/>
<node TEXT="# export requirements_&lt;yyyymm&gt;.txt" ID="ID_80233852" CREATED="1649592824613" MODIFIED="1649592851401"/>
<node TEXT="[-linux|-osx|-windows]" LOCALIZED_STYLE_REF="default" ID="ID_945021440" CREATED="1648840754952" MODIFIED="1649102752775" COLOR="#000000" BACKGROUND_COLOR="#ffffff" STYLE="fork">
<font BOLD="false"/>
<edge STYLE="bezier" COLOR="#808080"/>
</node>
</node>
<node TEXT="--yml_import" ID="ID_1607298486" CREATED="1651432083094" MODIFIED="1651432087482">
<node TEXT="# update/extend database from other environment.yml" ID="ID_752214196" CREATED="1649592871999" MODIFIED="1649592943809"/>
</node>
<node TEXT="--yml_export" ID="ID_830711686" CREATED="1651432087898" MODIFIED="1651432093400">
<node TEXT="# export environment_&lt;yyyymm&gt;.yml" ID="ID_1157909728" CREATED="1649592824613" MODIFIED="1649592974409"/>
<node TEXT="[-linux|-osx|-windows]" LOCALIZED_STYLE_REF="default" ID="ID_764191577" CREATED="1648840754952" MODIFIED="1649102752775" COLOR="#000000" BACKGROUND_COLOR="#ffffff" STYLE="fork">
<font BOLD="false"/>
<edge STYLE="bezier" COLOR="#808080"/>
</node>
</node>
<node TEXT="--packages_add" ID="ID_1017325688" CREATED="1651432469190" MODIFIED="1651432477570">
<node TEXT="P0 P1 .. Pn" LOCALIZED_STYLE_REF="default" FOLDED="true" ID="ID_512273540" CREATED="1649101691435" MODIFIED="1651432526205" COLOR="#000000" STYLE="fork">
<font BOLD="false"/>
<edge STYLE="bezier" COLOR="#808080"/>
<node TEXT="# call: pip check" ID="ID_350357728" CREATED="1649593165660" MODIFIED="1649593175853"/>
<node TEXT="# call: pip install .. and check sucess" ID="ID_1598755260" CREATED="1649593122392" MODIFIED="1649593164648"/>
<node TEXT="# call: pip check" ID="ID_1466786505" CREATED="1649593140178" MODIFIED="1649593148662"/>
<node TEXT="# update database" ID="ID_1705602847" CREATED="1649593149234" MODIFIED="1649593155355"/>
</node>
</node>
<node TEXT="--packages_delete" FOLDED="true" ID="ID_1590013358" CREATED="1651432478256" MODIFIED="1651432491565">
<node TEXT="P0 P1 .. Pn" LOCALIZED_STYLE_REF="default" FOLDED="true" ID="ID_857979055" CREATED="1649101695812" MODIFIED="1651432563274" COLOR="#000000" BACKGROUND_COLOR="#ffffff" STYLE="fork">
<font BOLD="false"/>
<edge STYLE="bezier" COLOR="#808080"/>
<node TEXT="# call: pip check" ID="ID_176542119" CREATED="1649593140178" MODIFIED="1649593148662"/>
<node TEXT="# warn, if P is dependency of other" ID="ID_928880018" CREATED="1649593204349" MODIFIED="1649593230112"/>
<node TEXT="# call: pip uninstall P" ID="ID_315330261" CREATED="1649593269824" MODIFIED="1649593277970"/>
<node TEXT="# call: pip check" ID="ID_1540657555" CREATED="1649593140178" MODIFIED="1649593148662"/>
<node TEXT="# update database" ID="ID_1447342363" CREATED="1649593149234" MODIFIED="1649593155355"/>
</node>
</node>
<node TEXT="--subset" ID="ID_759287554" CREATED="1651432606642" MODIFIED="1651432619041">
<node TEXT="P0 P1 P2 .. Pn" FOLDED="true" ID="ID_1453385721" CREATED="1649593305566" MODIFIED="1651432706038">
<node TEXT="[-name subset]" ID="ID_35328711" CREATED="1649593475937" MODIFIED="1649593553429">
<node TEXT="# default name of subset py_env_&lt;yyyymm&gt;_subset" ID="ID_911315223" CREATED="1649593503354" MODIFIED="1649593586088"/>
<node TEXT="# override, if needed" ID="ID_680146717" CREATED="1649593588562" MODIFIED="1649593597023"/>
</node>
<node TEXT="# extract P0..Pn with all dependencies" ID="ID_1562506979" CREATED="1649593335435" MODIFIED="1649593449242"/>
</node>
</node>
</node>
</node>
</node>
</map>
