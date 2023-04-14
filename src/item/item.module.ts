import { Module } from '@nestjs/common'
import { ItemController } from './item.controller'
import { ItemService } from './item.service'
import { TypeOrmModule } from '@nestjs/typeorm'
import { CategoryEntity } from './entities/category.entity'
import { ItemEntity } from './entities/item.entity'

@Module({
  imports: [TypeOrmModule.forFeature([CategoryEntity, ItemEntity])],
  controllers: [ItemController],
  providers: [ItemService],
  exports: [ItemService],
})
export class ItemModule {}
