import { Module } from '@nestjs/common'
import { CommentController } from './comment.controller'
import { CommentService } from './comment.service'
import { TypeOrmModule } from '@nestjs/typeorm'
import { CommentEntity } from './entities/comment.entity'
import { ItemModule } from '../item/item.module'
import { ItemEntity } from '../item/entities/item.entity'

@Module({
  imports: [TypeOrmModule.forFeature([CommentEntity, ItemEntity]), ItemModule],
  controllers: [CommentController],
  providers: [CommentService],
})
export class CommentModule {}
