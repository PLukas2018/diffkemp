```mermaid
---
# This code renders an image showingrankSpacing the relation of the commands.
# The image does not show on the GitHub app, use a browser to see the image.
config:
  theme: base
  themeVariables:
    nodeBorder: black
    mainBkg: white
    clusterBkg: white
    clusterBorder: black
    edgeLabelBackground: lightgrey
---
flowchart LR
subgraph G[" "]
  subgraph dk["DiffKemp"]
    sg -- "snapshots" --> sc -- "semantic differences" --> rv
    sg["1. Snapshot generation"]
    sc["2. Snapshot comparison"]
    rv["3. Result visualisation"]
    subgraph simpll["SimpLL"]
      ma("ModuleAnalysis")
      dfc("DifferentialFunctionComparator")
      cc("CustomPatternComparator")
      ma -.-> dfc -.-> cc
    end
  end
  subgraph llvm["LLVM project"]
    direction TB
    clang("clang -emit-llvm")
    opt("opt")
    fc("FunctionComparator")
    clang ~~~ opt ~~~ fc
  end
  sg -.-> clang
  sc -.-> simpll
  sg -.-> opt
  dfc -.-> fc
end
%% style
classDef mono font-family:monospace
class ccw,cg,ma,mc,dfc,fc,cc,clang,opt mono
```



Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Phasellus et lorem id felis nonummy placerat. Etiam ligula pede, sagittis quis, interdum ultricies, scelerisque eu. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Mauris metus. Nullam eget nisl. Aliquam id dolor. Duis risus. In dapibus augue non sapien. Integer malesuada. Nullam dapibus fermentum ipsum. In rutrum. Etiam quis quam. Phasellus faucibus molestie nisl. Donec quis nibh at felis congue commodo.

Duis risus. Aenean id metus id velit ullamcorper pulvinar. Nullam feugiat, turpis at pulvinar vulputate, erat libero tristique tellus, nec bibendum odio risus sit amet ante. Maecenas ipsum velit, consectetuer eu lobortis ut, dictum at dui. Aliquam ante. Nullam lectus justo, vulputate eget mollis sed, tempor sed magna. Vestibulum erat nulla, ullamcorper nec, rutrum non, nonummy ac, erat. Nunc dapibus tortor vel mi dapibus sollicitudin. Mauris tincidunt sem sed arcu. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos hymenaeos. Suspendisse nisl. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Integer imperdiet lectus quis justo. Curabitur sagittis hendrerit ante. Duis risus. Maecenas sollicitudin. Fusce nibh. Sed ac dolor sit amet purus malesuada congue. Proin in tellus sit amet nibh dignissim sagittis.

Fusce suscipit libero eget elit. Aliquam erat volutpat. Curabitur sagittis hendrerit ante. Quisque tincidunt scelerisque libero. Aliquam ante. Aliquam in lorem sit amet leo accumsan lacinia. Donec vitae arcu. In sem justo, commodo ut, suscipit at, pharetra vitae, orci. Nam quis nulla. Nullam dapibus fermentum ipsum. In laoreet, magna id viverra tincidunt, sem odio bibendum justo, vel imperdiet sapien wisi sed libero. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Nunc auctor. Etiam ligula pede, sagittis quis, interdum ultricies, scelerisque eu. Mauris tincidunt sem sed arcu. Vestibulum erat nulla, ullamcorper nec, rutrum non, nonummy ac, erat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Fusce consectetuer risus a nunc. Fusce nibh. Fusce tellus. Nam sed tellus id magna elementum tincidunt. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Proin pede metus, vulputate nec, fermentum fringilla, vehicula vitae, justo. Sed vel lectus. Donec odio tempus molestie, porttitor ut, iaculis quis, sem. Nullam faucibus mi quis velit. Aliquam erat volutpat. Fusce tellus odio, dapibus id fermentum quis, suscipit id erat. Sed elit dui, pellentesque a, faucibus vel, interdum nec, diam. Ut tempus purus at lorem. Integer rutrum, orci vestibulum ullamcorper ultricies, lacus quam ultricies odio, vitae placerat pede sem sit amet enim.

Nullam sit amet magna in magna gravida vehicula. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Vestibulum erat nulla, ullamcorper nec, rutrum non, nonummy ac, erat. Morbi leo mi, nonummy eget tristique non, rhoncus non leo. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos hymenaeos. Fusce nibh. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Suspendisse sagittis ultrices augue. Maecenas libero. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Pellentesque pretium lectus id turpis. Integer in sapien. Aenean placerat. Fusce suscipit libero eget elit. Morbi imperdiet, mauris ac auctor dictum, nisl ligula egestas nulla, et sollicitudin sem purus in lacus. Suspendisse sagittis ultrices augue.

Aliquam ante. Praesent id justo in neque elementum ultrices. Aenean id metus id velit ullamcorper pulvinar. Nullam dapibus fermentum ipsum. Duis sapien nunc, commodo et, interdum suscipit, sollicitudin et, dolor. Fusce nibh. Aliquam ante. Vestibulum fermentum tortor id mi. Sed convallis magna eu sem. Integer in sapien. Aliquam ornare wisi eu metus. Fusce tellus. Quisque tincidunt scelerisque libero. Duis viverra diam non justo. Etiam dictum tincidunt diam. Nullam eget nisl. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Donec quis nibh at felis congue commodo.

Etiam quis quam. Proin pede metus, vulputate nec, fermentum fringilla, vehicula vitae, justo. Aliquam erat volutpat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos hymenaeos. Fusce tellus. Phasellus rhoncus. Integer pellentesque quam vel velit. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Aliquam erat volutpat. Proin pede metus, vulputate nec, fermentum fringilla, vehicula vitae, justo. Fusce aliquam vestibulum ipsum. Integer lacinia. Sed ac dolor sit amet purus malesuada congue. Donec ipsum massa, ullamcorper in, auctor et, scelerisque sed, est. Aliquam id dolor. Nullam sapien sem, ornare ac, nonummy non, lobortis a enim. Pellentesque arcu. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.

Nulla est. Fusce suscipit libero eget elit. Integer vulputate sem a nibh rutrum consequat. Nulla est. Duis risus. Vestibulum fermentum tortor id mi. Et harum quidem rerum facilis est et expedita distinctio. Praesent vitae arcu tempor neque lacinia pretium. Nullam at arcu a est sollicitudin euismod. Etiam dictum tincidunt diam. Aliquam erat volutpat. Aliquam erat volutpat. Duis bibendum, lectus ut viverra rhoncus, dolor nunc faucibus libero, eget facilisis enim ipsum id lacus. Aenean id metus id velit ullamcorper pulvinar. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Etiam bibendum elit eget erat. Curabitur vitae diam non enim vestibulum interdum. Nullam rhoncus aliquam metus. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Nunc auctor. Et harum quidem rerum facilis est et expedita distinctio. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Duis bibendum, lectus ut viverra rhoncus, dolor nunc faucibus libero, eget facilisis enim ipsum id lacus. Fusce tellus odio, dapibus id fermentum quis, suscipit id erat. Proin mattis lacinia justo. Etiam dui sem, fermentum vitae, sagittis id, malesuada in, quam. Etiam bibendum elit eget erat. Aliquam erat volutpat. Vivamus porttitor turpis ac leo. In dapibus augue non sapien. Pellentesque arcu. Vivamus luctus egestas leo.

Aliquam in lorem sit amet leo accumsan lacinia. Maecenas fermentum, sem in pharetra pellentesque, velit turpis volutpat ante, in pharetra metus odio a lectus. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Nam quis nulla. Nullam rhoncus aliquam metus. Fusce nibh. Duis risus. Integer in sapien. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Etiam quis quam. In convallis. Aliquam in lorem sit amet leo accumsan lacinia. Vivamus porttitor turpis ac leo. Nullam sapien sem, ornare ac, nonummy non, lobortis a enim.

In sem justo, commodo ut, suscipit at, pharetra vitae, orci. Nulla turpis magna, cursus sit amet, suscipit a, interdum id, felis. Mauris tincidunt sem sed arcu. Etiam sapien elit, consequat eget, tristique non, venenatis quis, ante. Nulla pulvinar eleifend sem. In laoreet, magna id viverra tincidunt, sem odio bibendum justo, vel imperdiet sapien wisi sed libero. Nullam lectus justo, vulputate eget mollis sed, tempor sed magna. Sed vel lectus. Donec odio tempus molestie, porttitor ut, iaculis quis, sem. Quisque tincidunt scelerisque libero. Maecenas sollicitudin. Nulla est. Aenean vel massa quis mauris vehicula lacinia.

Fusce suscipit libero eget elit. In enim a arcu imperdiet malesuada. Quisque tincidunt scelerisque libero. Integer vulputate sem a nibh rutrum consequat. Vivamus luctus egestas leo. Proin pede metus, vulputate nec, fermentum fringilla, vehicula vitae, justo. Morbi imperdiet, mauris ac auctor dictum, nisl ligula egestas nulla, et sollicitudin sem purus in lacus. Nulla non lectus sed nisl molestie malesuada. Curabitur vitae diam non enim vestibulum interdum. Mauris elementum mauris vitae tortor. Pellentesque sapien. Maecenas aliquet accumsan leo. Mauris dictum facilisis augue. Nulla non lectus sed nisl molestie malesuada. Nullam lectus justo, vulputate eget mollis sed, tempor sed magna. Pellentesque sapien. Aliquam erat volutpat.

Pellentesque arcu. Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur? Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Etiam dictum tincidunt diam. Aliquam in lorem sit amet leo accumsan lacinia. Quisque tincidunt scelerisque libero. Nullam faucibus mi quis velit. Aenean placerat. Etiam dui sem, fermentum vitae, sagittis id, malesuada in, quam. In sem justo, commodo ut, suscipit at, pharetra vitae, orci. Praesent in mauris eu tortor porttitor accumsan. Proin pede metus, vulputate nec, fermentum fringilla, vehicula vitae, justo. Nulla est.

Duis condimentum augue id magna semper rutrum. Duis sapien nunc, commodo et, interdum suscipit, sollicitudin et, dolor. Fusce consectetuer risus a nunc. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos hymenaeos. Nulla est. Praesent dapibus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Etiam posuere lacus quis dolor. Mauris dolor felis, sagittis at, luctus sed, aliquam non, tellus. Maecenas sollicitudin.

Nullam dapibus fermentum ipsum. Nullam faucibus mi quis velit. Proin pede metus, vulputate nec, fermentum fringilla, vehicula vitae, justo. Maecenas aliquet accumsan leo. Duis ante orci, molestie vitae vehicula venenatis, tincidunt ac pede. Aliquam ante. Integer vulputate sem a nibh rutrum consequat. Etiam bibendum elit eget erat. Nunc auctor. Maecenas aliquet accumsan leo. Etiam posuere lacus quis dolor. Sed vel lectus. Donec odio tempus molestie, porttitor ut, iaculis quis, sem. Integer imperdiet lectus quis justo. Nulla quis diam. Sed elit dui, pellentesque a, faucibus vel, interdum nec, diam. Ut tempus purus at lorem. Nullam faucibus mi quis velit. Aliquam id dolor. Nunc dapibus tortor vel mi dapibus sollicitudin.

Etiam bibendum elit eget erat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Mauris metus. Cras elementum. Phasellus et lorem id felis nonummy placerat. Sed vel lectus. Donec odio tempus molestie, porttitor ut, iaculis quis, sem. Maecenas ipsum velit, consectetuer eu lobortis ut, dictum at dui. Praesent vitae arcu tempor neque lacinia pretium. Pellentesque sapien. Etiam posuere lacus quis dolor. In enim a arcu imperdiet malesuada. Donec iaculis gravida nulla. Proin mattis lacinia justo.

Etiam dictum tincidunt diam. Sed elit dui, pellentesque a, faucibus vel, interdum nec, diam. Quisque porta. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Etiam ligula pede, sagittis quis, interdum ultricies, scelerisque eu. Integer rutrum, orci vestibulum ullamcorper ultricies, lacus quam ultricies odio, vitae placerat pede sem sit amet enim. Donec quis nibh at felis congue commodo. Nunc auctor. Etiam sapien elit, consequat eget, tristique non, venenatis quis, ante. Proin mattis lacinia justo. Sed convallis magna eu sem. Morbi scelerisque luctus velit. Maecenas aliquet accumsan leo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Duis condimentum augue id magna semper rutrum. Fusce wisi.

Maecenas libero. Proin pede metus, vulputate nec, fermentum fringilla, vehicula vitae, justo. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Vivamus porttitor turpis ac leo. Etiam posuere lacus quis dolor. Proin pede metus, vulputate nec, fermentum fringilla, vehicula vitae, justo. Integer rutrum, orci vestibulum ullamcorper ultricies, lacus quam ultricies odio, vitae placerat pede sem sit amet enim. Duis pulvinar. Duis ante orci, molestie vitae vehicula venenatis, tincidunt ac pede. Curabitur bibendum justo non orci. In dapibus augue non sapien. Nunc auctor. Duis sapien nunc, commodo et, interdum suscipit, sollicitudin et, dolor. Cras elementum. In convallis. Donec ipsum massa, ullamcorper in, auctor et, scelerisque sed, est.

Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Fusce consectetuer risus a nunc. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce tellus. Sed vel lectus. Donec odio tempus molestie, porttitor ut, iaculis quis, sem. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Nunc auctor. Nullam feugiat, turpis at pulvinar vulputate, erat libero tristique tellus, nec bibendum odio risus sit amet ante. Fusce tellus odio, dapibus id fermentum quis, suscipit id erat. Vivamus luctus egestas leo. Quisque tincidunt scelerisque libero. Duis pulvinar. Integer lacinia. Aliquam id dolor. Phasellus et lorem id felis nonummy placerat.

Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos hymenaeos. Duis bibendum, lectus ut viverra rhoncus, dolor nunc faucibus libero, eget facilisis enim ipsum id lacus. Quisque porta. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer tempor. Aliquam ante. Nulla non lectus sed nisl molestie malesuada. Mauris tincidunt sem sed arcu. Nullam dapibus fermentum ipsum. Suspendisse nisl. Duis risus. Pellentesque pretium lectus id turpis. Pellentesque ipsum. Mauris elementum mauris vitae tortor. Integer malesuada. Nullam at arcu a est sollicitudin euismod.

## snapshot creation

tdd
